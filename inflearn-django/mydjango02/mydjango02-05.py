# pip install "django~=4.2.0"
# pip install requests

import sys
import django
import requests
import sqlite3
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

    song_list = get_song_list(query)

    return render(
        request,
        "index.html",
        {"song_list": song_list, "query": query},
    )


def get_song_list(query: str):
    connecton = sqlite3.connect("melon-20230906.sqlite3")
    cursor = connecton.cursor()
    connecton.set_trace_callback(print)

    if query:
        param = "%" + query + "%"
        sql = "SELECT * FROM songs WHERE 가수 LIKE ? OR 곡명 LIKE ?"
        cursor.execute(sql, (param, param))
    else:
        cursor.execute("SELECT * FROM songs")

    column_names = [desc[0] for desc in cursor.description]

    # list comprehension
    song_list = [
        dict(zip(column_names, song_tuple)) for song_tuple in cursor.fetchall()
    ]

    connecton.close()
    return song_list


urlpatterns = [
    path("", index),
]

execute_from_command_line(sys.argv)
