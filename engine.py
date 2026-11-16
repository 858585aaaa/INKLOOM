import os, json, re
from django.conf import settings

def analyze_content(item):
    # Deterministic checks run without an API key, so the core product remains usable offline.
    text = item.body
    findings = []
    rules = item.brand.guidelines.filter(is_active=True)
    for rule in rules:
        if rule.rule_type == "restricted_word":
            terms = [x.strip() for x in re.split(r"[,;\\n]", rule.content) if x.strip()]
            for term in terms:
                match = re.search(r"(?i)\b" + re.escape(term) + r"\b", text)
                if match:
                    findings.append({
                        "guideline":rule, "severity":"high", "title":f"Restricted term: {term}",
                        "explanation":f'The text contains “{term}”, which is restricted by the brand rule “{rule.title}”.',
                        "matched_text":match.group(0),
                        "suggestion":rule.replacement or "Replace this term with wording approved by the brand owner."
                    })
        elif rule.rule_type == "preferred_word":
            # A preferred-word rule is phrased as: preferred term; alternatives to avoid.
            parts = [x.strip() for x in re.split(r"[,;]", rule.content) if x.strip()]
            if len(parts) >= 2:
                preferred, avoid = parts[0], parts[1:]
                for term in avoid:
                    match = re.search(r"(?i)\b" + re.escape(term) + r"\b", text)
                    if match:
                        findings.append({
                            "guideline":rule, "severity":"medium", "title":f"Use preferred wording: {preferred}",
                            "explanation":f'“{term}” appears, but this brand prefers “{preferred}”.',
                            "matched_text":match.group(0), "suggestion":f"Consider replacing it with “{preferred}”."
                        })
        elif rule.rule_type == "approved_fact":
            # Approved facts are guidance context; do not assert unsupported factual mismatches automatically.
            continue
    for rule in rules.filter(rule_type__in=["tone_rule","general_rule"]):
        if rule.content.strip().lower().startswith("avoid exclamation"):
            if "!" in text:
                findings.append({"guideline":rule,"severity":"low","title":"Tone guideline check",
                    "explanation":f'The content uses exclamation marks, while “{rule.title}” advises against them.',
                    "matched_text":"!","suggestion":"Consider using a full stop or calmer wording."})
    score = max(0, 100 - sum({"high":20,"medium":10,"low":5,"info":0}[f["severity"]] for f in findings))
    source = "Rule-based analysis"
    # Optional Gemini enhancement. Fail safely to deterministic results if unavailable.
    api_key = os.getenv("GEMINI_API_KEY", "")
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            rules_text = "\\n".join([f"- {r.get_rule_type_display()}: {r.title}: {r.content}" for r in rules])
            prompt = (
                "Review the marketing content against the brand rules. Return ONLY a JSON array of objects "
                "with keys severity (high/medium/low/info), title, explanation, matched_text, suggestion. "
                "Do not invent brand facts. Only report clear issues. If no issues, return [].\\n"
                f"BRAND: {item.brand.name}\\nRULES:\\n{rules_text}\\nCONTENT:\\n{text}"
            )
            response = client.models.generate_content(model=os.getenv("GEMINI_MODEL","gemini-2.5-flash"), contents=prompt)
            raw = (response.text or "").strip().replace("```json","").replace("```","").strip()
            extra = json.loads(raw)
            if isinstance(extra, list):
                existing = {(f["title"], f["matched_text"]) for f in findings}
                for f in extra[:12]:
                    if not isinstance(f, dict): continue
                    sev = f.get("severity","info")
                    if sev not in {"high","medium","low","info"}: sev = "info"
                    title = str(f.get("title","AI observation"))[:180]
                    matched = str(f.get("matched_text",""))[:240]
                    if (title,matched) not in existing:
                        findings.append({"guideline":None,"severity":sev,"title":title,
                            "explanation":str(f.get("explanation",""))[:1500],
                            "matched_text":matched,"suggestion":str(f.get("suggestion",""))[:300]})
                source = "Rule checks + Gemini AI"
        except Exception:
            source = "Rule-based analysis (Gemini unavailable; fallback used)"
    score = max(0, 100 - sum({"high":20,"medium":10,"low":5,"info":0}[f["severity"]] for f in findings))
    return findings, score, source
