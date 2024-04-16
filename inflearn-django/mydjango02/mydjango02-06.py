import sys
import django
import requests
from django.db import connection
from django.conf import settings
from django.core.management import execute_from_command_line
from django.shortcuts import render
from django.urls import path


settings.configure(
    ROOT_URLCONF=__name__,
    DEBUG=True,
    SECRET_KEY="secret",
    # db 설정 추가
    # 멀티 데이터베이스 지원(여러 데이터벵스 엔진에 대해서 여러 연결 설정을 정의할 수 있음
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "melon-20230906.sqlite3",  # sqllite는 db이름이 없는 파일 db 이기 때문에 경로를 지정
        },
    },
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

    song_list = get_song_list(query)

    return render(
        request,
        "index.html",
        {"song_list": song_list, "query": query},
    )


def get_song_list(query: str):
    cursor = connection.cursor()

    if query:
        param = "%" + query + "%"
        sql = "SELECT * FROM songs WHERE 가수 LIKE %s OR 곡명 LIKE %s"  # sql 자체는 db 종류에 딷라 다를 수 있다
        cursor.execute(sql, (param, param))
    else:
        cursor.execute("SELECT * FROM songs")

    column_names = [desc[0] for desc in cursor.description]

    # list comprehension
    song_list = [
        dict(zip(column_names, song_tuple)) for song_tuple in cursor.fetchall()
    ]

    return song_list


urlpatterns = [
    path("", index),
]

execute_from_command_line(sys.argv)
