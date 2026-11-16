from django.db import models
from brands.models import Brand
class Guideline(models.Model):
    TYPE_CHOICES = [
        ("approved_fact","Approved fact"),("preferred_word","Preferred word"),
        ("restricted_word","Restricted word"),("tone_rule","Tone rule"),("general_rule","General guideline")
    ]
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="guidelines")
    rule_type = models.CharField(max_length=24, choices=TYPE_CHOICES)
    title = models.CharField(max_length=140)
    content = models.TextField()
    replacement = models.CharField(max_length=180, blank=True)
    source_note = models.CharField(max_length=240, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ["rule_type","title"]
    def __str__(self): return f"{self.brand.name}: {self.title}"
