from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from hottrack.models import Song
from hottrack.utils.cover import make_cover_image


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


def cover_png(request, pk):
    # 최댓값 512, 기본값 256
    # http://127.0.0.1:8000/hottrack/501/cover.png?size=512 이렇게 요청되어 들어온 경우
    # size에 해당하는 값을 사용하고 제공되지 않은 경우 기본값 256을 사용함
    canvas_size = min(512, int(request.GET.get("size", 256)))

    # pk가 일치하는 객체를 찾으면 해당 객체 반환 아니면 404
    song = get_object_or_404(Song, pk=pk)

    cover_image = make_cover_image(
        song.cover_url, song.artist_name, canvas_size=canvas_size
    )

    # param fp : filename (str), pathlib.Path object or file object
    # image.save("image.png")
    response = HttpResponse(content_type="image/png")
    cover_image.save(response, format="png")

    return response
