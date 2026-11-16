from django.test import TestCase
from django.contrib.auth.models import User
from brands.models import Brand
from guidelines.models import Guideline
from content_review.models import ContentItem
from content_review.engine import analyze_content

class RuleEngineTests(TestCase):
    def test_restricted_word_is_flagged(self):
        user = User.objects.create_user(username="tester", password="StrongPass123!")
        brand = Brand.objects.create(owner=user, name="Demo", industry="Retail", description="Demo brand")
        Guideline.objects.create(brand=brand, rule_type="restricted_word", title="Avoid claims",
                                 content="guaranteed, miracle", replacement="may help")
        item = ContentItem.objects.create(owner=user, brand=brand, title="Test", body="This is guaranteed to work.")
        findings, score, source = analyze_content(item)
        self.assertTrue(any("guaranteed" in f["title"].lower() for f in findings))
        self.assertLess(score, 100)
