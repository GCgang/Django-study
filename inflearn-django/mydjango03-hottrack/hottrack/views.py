import json
from urllib.request import urlopen  # URL을 통해 원격 데이터에 접근할 수 있게 해준다

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from hottrack.models import Song


# 타입을 지정하면 이상한 타입추론도 줄이고 보다 빠르고 정확하게 자동완성을 제공받을 수 있다
def index(request: HttpRequest) -> HttpResponse:  # view 함수의 반환 타입은 HttpResponse
    query = request.GET.get("query", "").strip()

    melon_chart_url = "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/melon/melon-20230910.json"
    # urlopen: URL을 인자로 받고, 그 URL에 해당하는 서버에 HTTP 요청을 보내고, 서버로부터의 응답을 받는 객체를 반환한다
    # read(): 해당 객체의 내용을 바이트 스트림으로 읽음
    # decode("utf-8"): 바이트 형식으로 받아온 데이터를 인코딩하여 문자열로 변환
    json_string = urlopen(melon_chart_url).read().decode("utf-8")

    # 외부 필드명을 그대로 쓰기보다, 내부적으로 사용하는 필드명으로 변경하고, 필요한 메서드를 추가합니다.
    # json.loads(json_string): json_string을 파이썬 딕셔너리로 반환
    song_list = [Song.from_dict(song_dict) for song_dict in json.loads(json_string)]

    if query:
        song_list = [
            song
            for song in song_list
            if (
                (query in song.name)
                or (query in song.artist_name)
                or (query in song.album_name)
                # or (query in song.lyrics)
            )
        ]

    return render(
        request=request,
        template_name="hottrack/index.html",
        context={"song_list": song_list, "query": query},
    )
