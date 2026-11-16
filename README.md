# INKLOOM AI — Complete Hackathon Project

A Django-based brand governance MVP with user accounts, brand profiles, brand guidelines, content submission, deterministic rule analysis, optional Gemini-assisted review, human decisions and review history.

## Features
- Registration, login, logout and owner-protected workspace
- Create, view, edit and delete multiple brand profiles
- Guidelines: approved facts, preferred words, restricted words, tone rules and general rules
- Submit content for a selected brand/channel
- Rule-based analysis works without an API key
- Optional Gemini enhancement when `GEMINI_API_KEY` is configured
- Findings with severity, explanation, matched text and suggestion
- Revise and re-analyze content
- Human approve / request revision / reject actions
- Review event history and dashboard metrics
- Per-user data access checks

## Windows setup (VS Code)
1. Extract ZIP to a new folder and open that folder in VS Code.
2. Open Terminal in the project folder.
3. Create and activate environment:
   `py -m venv .venv`
   `.venv\\Scripts\\activate`
4. Install packages:
   `python -m pip install --upgrade pip`
   `pip install -r requirements.txt`
5. Copy `.env.example` to `.env`. Keep `GEMINI_API_KEY` blank if you do not have one.
6. Create tables and start:
   `python manage.py makemigrations brands guidelines content_review`
   `python manage.py migrate`
   `python manage.py runserver`
7. Open http://127.0.0.1:8000/

## Suggested end-to-end test
1. Register a new user and sign in.
2. Create a brand profile.
3. Open the brand and add a Restricted Word rule. Example: rule type `Restricted word`, title `Avoid unsupported superlatives`, content `guaranteed, miracle`, replacement `designed to help`.
4. Add a Preferred Word rule. Enter content as `customers, buyers, shoppers` (preferred term first, alternatives after).
5. Submit content containing one of the restricted terms.
6. Open findings, inspect explanations/suggestions, edit the text and re-analyze.
7. Use Approve, Request revision or Reject and inspect Review history.

## Important product limitations
- Approved facts are stored as trusted context but the MVP does not automatically fact-check claims against external sources.
- Tone and general rules are not interpreted as broadly as a human editor; only clear configured rules are checked deterministically.
- Gemini is optional and may fail due to quota, network or model availability; the rule engine remains available as fallback.
- Human review actions in this MVP are performed by the signed-in content owner, not a separate role-based reviewer account.
- Before public deployment, add production database, secure secret management, HTTPS, rate limiting, tests, backups and role-based permissions.

## Hackathon integrity
Use only during the official build window. Keep evidence of work, commit changes to Git during the event, and disclose AI assistance/tools as required by the organisers. This is a starter implementation and must be run and tested by your team before claiming completion.


## Homepage
The public landing page is `templates/index.html`. Django serves this page at the site root (`/`).
