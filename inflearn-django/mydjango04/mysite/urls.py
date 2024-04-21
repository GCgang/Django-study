from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path(route="core/", view=include("core.urls")),
    path(route="", view=lambda request: redirect("core/")),
]
