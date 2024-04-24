import pandas as pd
import datetime

from django.db.models import QuerySet, Q
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from io import BytesIO
from typing import Literal
from hottrack.models import Song
from hottrack.utils.cover import make_cover_image
from django.views.generic import DetailView

# 타입을 지정하면 이상한 타입추론도 줄이고 보다 빠르고 정확하게 자동완성을 제공받을 수 있다
def index(request: HttpRequest, release_date: datetime.date = None) -> HttpResponse:  # view 함수의 반환 타입은 HttpResponse
    query = request.GET.get("query", "").strip()

    song_qs: QuerySet = Song.objects.all()
    
    if release_date:
        song_qs = song_qs.filter(release_date=release_date)

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

song_detail = DetailView.as_view(
    # 해당 뷰는 URL CapturedValues 중에서 pk 혹은 melon_uid 이름의 값만 지원하며, 
    # slug 대신에 melon_uid를 사용하도록 설정했기 때문에, slug 값은 지원하지 않는다
    model=Song,
    slug_field="melon_uid",
    slug_url_kwarg="melon_uid",
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


# 데이터를 CSV 또는 Excel 형식으로 내보내는 함수
def export(request: HttpRequest, format: Literal["csv", "xlsx"]) -> HttpResponse:
    song_qs = QuerySet = Song.objects.all()

    # .valuse() : 지정한 필드로 구성된 사전 리스트를 반환
    song_qs = song_qs.values()
    # 원하는 필드만 지정해서 뽑을 수도 있다.
    # song_qs = song_qs.values("rank", "name", "artist_name", "like_count")

    # 사전 리스트를 인자로 받아서, DataFrame을 생성할 수 있다
    df = pd.DataFrame(data=song_qs)

    # 메모리 파일 객체에 CSV 데이터 저장
    # CSV를 HttpResponse에 바로 저장할 떄 utf-8-sig 인코딩이 적용되지 않아서
    # BytesIO를 사용하여 인코딩을 적용한 후, HttpResponse에 저장한다
    export_file = BytesIO()

    if format == "csv":
        content_type = "text/csv"
        filename = "hottrack.csv"
        # df.to_csv("hottrack.csv", index=False)      # 지정 파일로 저장할 수도 있고, 파일 객체를 전달할 수도 있다.
        # (한글깨짐방지) 한글 엑셀에서는 CSV 텍스트 파일을 해석하는 기본 인코딩이 cp949이기에
        # utf-8-sig 인코딩을 적용하여 생성되는 CSV 파일에 UTF-8 BOM이 추가한다.
        df.to_csv(path_or_buf=export_file, index=False, encoding="utf-8-sig")  # noqa
    elif format == "xlsx":
        # .xls : application/vnd.ms-excel
        content_type = (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # xlsx
        )
        filename = "hottrack.xlsx"
        df.to_excel(excel_writer=export_file, index=False, engine="openpyxl")  # noqa
    else:
        return HttpResponseBadRequest(f"Invalid format : {format}")

    # 저장된 파일의 전체 내용을 HttpResponse에 전달
    response = HttpResponse(content=export_file.getvalue(), content_type=content_type)

    # Content-Disposition 헤더를 설정하여 브라우저가 해당 파일을 다운로드할 수 있도록 한다.
    response["Content-Disposition"] = "attachment; filename*=utf-8''{}".format(filename)

    return response
