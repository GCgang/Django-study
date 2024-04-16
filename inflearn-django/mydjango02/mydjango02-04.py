import sys
import django
import requests
from django.conf import settings
from django.core.management import execute_from_command_line
from django.shortcuts import render
from django.urls import path


settings.configure(
    ROOT_URLCONF=__name__,
    DEBUG=True,
    SECRET_KEY="secret",
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["templates"],
        }
    ],
)
django.setup()


def index(request):
    # 주소 뒤에 물음표 뒤에 붙어있는 문자열을 Query String이라고 하는데 장고에서는 가공된 값을 request.GET 사전으로 읽어올 수 있다
    query = request.GET.get("query", "").strip()  # 검색어

    json_url = "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/melon/melon-20230906.json"

    response = requests.get(json_url)
    # response.raise_for_status()  # 비정상 응답을 받으면 HTTPError을 발생

    if response.ok:  # 응답이 정상이라면
        song_list = response.json()
    else:  # django messages 프레임워크를 활용하면 "리소스 없음" 등의 메시지를 보여줄 수 있다
        song_list = []

    # 검색어가 있다면 해당하는 가수의 노래를 보여줌
    # 빈 문자열인 경우 False 판정으로 전체 리스트를 보여준다
    if query:
        song_list = filter(
            lambda song: query in song["가수"],
            song_list,
        )

    return render(
        request,
        template_name="index.html",
        context={"song_list": song_list, "query": query},
    )


urlpatterns = [
    path("", index),
]

execute_from_command_line(sys.argv)
