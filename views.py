from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from brands.models import Brand
from .forms import GuidelineForm
from .models import Guideline
def owned_brand(user, brand_pk):
    return get_object_or_404(Brand, pk=brand_pk, owner=user)
@login_required
def guideline_list(request, brand_pk):
    brand = owned_brand(request.user, brand_pk)
    items = brand.guidelines.all()
    return render(request, "guidelines/guideline_list.html", {"brand":brand,"guidelines":items})
@login_required
def guideline_create(request, brand_pk):
    brand = owned_brand(request.user, brand_pk); form = GuidelineForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False); item.brand = brand; item.save()
        messages.success(request, "Guideline saved."); return redirect("guideline_list", brand_pk=brand.pk)
    return render(request, "guidelines/guideline_form.html", {"brand":brand,"form":form,"page_title":"Add guideline"})
@login_required
def guideline_edit(request, brand_pk, pk):
    brand = owned_brand(request.user, brand_pk); item = get_object_or_404(Guideline, pk=pk, brand=brand)
    form = GuidelineForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save(); messages.success(request, "Guideline updated."); return redirect("guideline_list", brand_pk=brand.pk)
    return render(request, "guidelines/guideline_form.html", {"brand":brand,"form":form,"page_title":"Edit guideline"})
@login_required
def guideline_delete(request, brand_pk, pk):
    brand = owned_brand(request.user, brand_pk); item = get_object_or_404(Guideline, pk=pk, brand=brand)
    if request.method == "POST":
        item.delete(); messages.success(request, "Guideline deleted.")
    return redirect("guideline_list", brand_pk=brand.pk)
