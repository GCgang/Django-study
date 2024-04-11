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
# 하드코딩한 html 파일 반환하기
def index(request):
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
            width: 100%;
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
            <tr><td>Seven (feat. Latto) - Clean Ver.</td><td>정국</td></tr>
            <tr><td>Love Lee</td><td>AKMU (악뮤)</td></tr>
            <tr><td>Super Shy</td><td>NewJeans</td></tr>
            <tr><td>후라이의 꿈</td><td>AKMU (악뮤)</td></tr>
            <tr><td>어떻게 이별까지 사랑하겠어, 널 사랑하는 거지</td><td>AKMU (악뮤)</td></tr>
        </tbody>
    </table>

</body>
</html>
    """
    )


# View 함수
def hello(request):
    return HttpResponse("hello django")


urlpatterns = [
    path("", index),
    path("hello/", hello),
]


execute_from_command_line(sys.argv)
