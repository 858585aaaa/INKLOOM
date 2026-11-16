from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("brands/", include("brands.urls")),
    path("brands/<int:brand_pk>/guidelines/", include("guidelines.urls")),
    path("content/", include("content_review.urls")),
]
