# pip install "django~=4.2.0"
# pip install requests

import sys
import django
import requests
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.management import execute_from_command_line
from django.shortcuts import render
from django.urls import path
from django.http import JsonResponse



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


class Song(models.Model):
    id = models.AutoField(primary_key=True)
    가수 = models.CharField(max_length=100)
    곡명 = models.CharField(max_length=200)
    곡일련번호 = models.IntegerField()
    순위 = models.IntegerField()
    앨범 = models.CharField(max_length=200)
    좋아요 = models.IntegerField()
    커버이미지_주소 = models.URLField()

    def __str__(self):
        return self.곡명

    class Meta:
        db_table = "songs"
        app_label = "melon"


def index(request):

    return render(
        request,
        template_name= "index.html",
    )

def song_list_api(request):
        # 주소 뒤에 물음표 뒤에 붙어있는 문자열을 Query String이라고 하는데 장고에서는 가공된 값을 request.GET 사전으로 읽어올 수 있다
    query = request.GET.get("query", "").strip()  # 검색어

    song_list = Song.objects.all()  # 변수명은 _list 이지만 QuerySet 객체 반환

    if query:
        # QuerySet 객체를 통해 조회 조건을 추가할 수 있음
        song_list = song_list.filter(
            Q(곡명__icontains=query) | Q(가수__icontains=query)
        )
    song_list_data = list(song_list.values())

    return JsonResponse(
        song_list_data,
        safe=False,
        json_dumps_params={"ensure_ascii": False},
        content_type="application/json; charset=utf-8",
    )

urlpatterns = [
    path("", index),
    path("api/song-list.json", song_list_api),
]

execute_from_command_line(sys.argv)
