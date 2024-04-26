from django.urls import path, re_path
from . import converters
from . import views

urlpatterns = [
    path(route="", view=views.index),
    path(route="<int:pk>/", view=views.song_detail),
    path(route="melon-<int:melon_uid>/", view=views.song_detail),
    path(route="archives/<date:release_date>/", view=views.index),
    path(route="<int:pk>/cover.png", view=views.cover_png),
    re_path(
        route=r"^export\.(?P<format>(csv|xlsx))$", view=views.export, name="export"
    ),
    re_path(
        route=r"^archives/(?P<year>\d{4})/(?P<date_list_period>year|month|day|week)?/?$",
        view=views.SongYearArchiveView.as_view(),
        name="song_archive_year",
    ),
]
