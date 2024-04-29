from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Dict
from django.urls import reverse
from django.utils.text import slugify

# url에서 사용할 수 있는 안전한 형태의 문자열로 인코딩 하는 역할
from urllib.parse import quote

from django.db import models


class Song(models.Model):
    melon_uid = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True) # 한글 지원을 위해 allow_unicode 옵션을 켜준다
    rank = models.PositiveSmallIntegerField()
    album_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    artist_name = models.CharField(max_length=100)
    cover_url = models.URLField()
    lyrics = models.TextField()
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    like_count = models.PositiveIntegerField()

    class Meta:
        # 조회를 위해 인덱스를 추가한다
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        # slug 필드는 name 필드에 의존적이다
        # slug 필드 값이 없는 경우에만 name 필드로부터 slug 필드를 채운다
        self.slugify()
        super().save(*args, **kwargs)

    def slugify(self, force=False):
        if force or not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
            # 현재 모델의 slug 필드의 max_length가 변할 수 있기 때문에 상수값 적지않고 아래와 같이 작성
            slug_max_length = self._meta.get_field("slug").max_length
            self.slug = self.slug[:slug_max_length]

    def get_absolute_url(self) -> str:
        return reverse(
            "hottrack:song_detail",
            args=[
                self.release_date.year,
                self.release_date.month,
                self.release_date.day,
                self.slug,
            ],
        )
    
    # property 데코레이터를 사용하여 메소드를 속성처럼 접근할 수 있게 한다
    @property
    def melon_detail_url(self) -> str:
        melon_uid = quote(self.melon_uid)
        return f"https://www.melon.com/song/detail.htm?songId={melon_uid}"

    @property
    def youtube_search_url(self) -> str:
        search_query = quote(f"{self.name}, {self.artist_name}")
        return f"https://www.youtube.com/results?search_query={search_query}"

    @classmethod
    def from_dict(cls, data: Dict) -> Song:
        isinstance = cls(
            melon_uid=data.get("곡일련번호"),
            rank=int(data.get("순위")),
            album_name=data.get("앨범"),
            name=data.get("곡명"),
            artist_name=data.get("가수"),
            cover_url=data.get("커버이미지_주소"),
            lyrics=data.get("가사"),
            genre=data.get("장르"),
            release_date=date.fromisoformat(data.get("발매일")),
            like_count=int(data.get("좋아요")),
        )
        isinstance.slugify()
        return isinstance
