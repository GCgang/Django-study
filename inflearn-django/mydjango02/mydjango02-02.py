# pip install "django~=4.2.0"

import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path

settings.configure(
    ROOT_URLCONF=__name__,
    DEBUG=True,
    SECRET_KEY="secret",
)
django.setup()


# View 함수 : HTTP 요청이 올 때마다 호출 되어, 요청을 처리하여 응답을 생성/반환하는 함수
# 곡 목록 리스트를 파이썬 리스트로 따로 관리하고 HTML 문자열을 동적으로 조합 하고 조건문으로 특정 가수만 필터링 하기
def index(request):
    song_list = [
        {"곡명": "Seven (feat. Latto) - Clean Ver.", "가수": "정국"},
        {"곡명": "Love Lee", "가수": "AKMU (악뮤)"},
        {"곡명": "Super Shy", "가수": "NewJeans"},
        {"곡명": "후라이의 꿈", "가수": "AKMU (악뮤)"},
        {"곡명": "어떻게 이별까지 사랑하겠어, 널 사랑하는 거지", "가수": "AKMU (악뮤)"},
    ]

    partial_html = "".join(
        f"<tr><td>{song['곡명']}</td><td>{song['가수']}</td></tr>"
        for song in song_list
        if song["가수"] == "정국"
    )

    return HttpResponse(
        """
<!doctype html>
<html lang="ko">
<head>
    <meta charset="UTF-8" />
    <title>Melon List</title>
    <style>
        body {
            width: 400px;
            margin: 0 auto;
        }
        table {
            width: 100%%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
    </style>
</head>
<body>
    <h1>Melon List</h1>
    <table>
        <thead>
            <tr><th>곡명</th><th>가수</th></tr>
        </thead>
        <tbody>
            %s
        </tbody>
    </table>
</body>
</html>
    """
        % (partial_html,)
    )


# View 함수
def hello(request):
    return HttpResponse("hello django")


urlpatterns = [
    path("", index),
    path("hello/", hello),
]


execute_from_command_line(sys.argv)
