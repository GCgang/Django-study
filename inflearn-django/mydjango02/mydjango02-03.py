# pip install "django~=4.2.0"

import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path

settings.configure(
    ROOT_URLCONF=__name__,
    DEBUG=True,
    SECRET_KEY="secret",
    # 복잡한 문자열 조합을 파이썬 코드 만으로 수행하는 것은 한계가 있어,
    # 템플릿 엔진을 활용하면 복잡한 문자열도 체계적으로 조합할 수 있다.
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["templates"],
        }
    ],
)
django.setup()


# View 함수 : HTTP 요청이 올 때마다 호출 되어, 요청을 처리하여 응답을 생성/반환하는 함수
def index(request):
    query = "악뮤"  # 검색어
    song_list = [
        {"곡명": "Seven (feat. Latto) - Clean Ver.", "가수": "정국"},
        {"곡명": "Love Lee", "가수": "AKMU (악뮤)"},
        {"곡명": "Super Shy", "가수": "NewJeans"},
        {"곡명": "후라이의 꿈", "가수": "AKMU (악뮤)"},
        {"곡명": "어떻게 이별까지 사랑하겠어, 널 사랑하는 거지", "가수": "AKMU (악뮤)"},
    ]
    # 파이썬 빌트인 함수 filter를 활용하여, 곡명에 검색어가 포함된 노래만 필터링
    song_list = filter(
        lambda song: query in song["가수"] or query in song["곡명"], song_list
    )

    # render가 지정 이름의 템플릿을 사용해서 HttpResponse 응답을 만들어낸다
    return render(request, "index.html", {"song_list": song_list})


# View 함수
def hello(request):
    return HttpResponse("hello django")


urlpatterns = [
    path("", index),
    path("hello/", hello),
]


execute_from_command_line(sys.argv)
