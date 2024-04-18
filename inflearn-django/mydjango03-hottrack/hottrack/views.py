from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from hottrack.models import Song


# 타입을 지정하면 이상한 타입추론도 줄이고 보다 빠르고 정확하게 자동완성을 제공받을 수 있다
def index(request: HttpRequest) -> HttpResponse:  # view 함수의 반환 타입은 HttpResponse
    query = request.GET.get("query", "").strip()

    song_qs: QuerySet = Song.objects.all()

    if query:
        song_qs = song_qs.filter(
            Q(name__icontains=query)
            | Q(artist_name__icontains=query)
            | Q(album_name__icontains=query)
        )
    return render(
        request=request,
        template_name="hottrack/index.html",
        context={"song_list": song_qs, "query": query},
    )
