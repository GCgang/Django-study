from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

# from hottrack.views import index

urlpatterns = [
    path(route="admin/", view=admin.site.urls),
    path(route="hottrack/", view=include("hottrack.urls")),
    path(route="", view=lambda request: redirect("/hottrack/")),
    # path(route="hottrack/", view=index),
]
