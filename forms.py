from django import forms
from .models import Guideline
class GuidelineForm(forms.ModelForm):
    class Meta:
        model = Guideline
        fields = ["rule_type","title","content","replacement","source_note","is_active"]
        widgets = {
            "rule_type":forms.Select(attrs={"class":"form-select"}),
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "content":forms.Textarea(attrs={"class":"form-control","rows":4}),
            "replacement":forms.TextInput(attrs={"class":"form-control"}),
            "source_note":forms.TextInput(attrs={"class":"form-control"}),
            "is_active":forms.CheckboxInput(attrs={"class":"form-check-input"}),
        }
