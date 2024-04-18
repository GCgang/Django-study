from django.contrib import admin
from django.utils.html import format_html
from hottrack.models import Song  # from .models import Song
from hottrack.utils.melon import get_likes_dict


# list_display 속성에 지정하는 이름들은
# 1) Model 클래스의 필드면
# 2) Model 클래스의 인자없는 함수
# 3) Model 클래스의 커스텀 속성
# 4) ModelAdmin 클래스의 인자 1개 받는 함수
# 들의 이름을 지정할 수 있다
@admin.register(
    Song
)  # 이 데코레이터는 Song 모델을 Django 관리자 페이지에 등록한다. 이렇게 하면 Song 모델을 관리자 페이지에서 볼 수 있다.
class SongAdmin(admin.ModelAdmin):
    # 검색시에 검색을 수행할 필드명 목록을 지정  # where
    search_fields = [
        "name",
        "artist_name",
        "album_name",
    ]
    # 목록에 표시할 필드
    list_display = [
        "cover_image",
        "name",
        "artist_name",
        "album_name",
        "genre",
        "like_count",
        "release_date",
    ]
    # 지정된 필드가 어떤 값을 가진 필드라면, 그 필드의 값들로 필터링 선택지를 구성
    # 지정된 필드가 DateField 라면 오늘, 지난 7일, 이번달, 올해 선택지를 구성
    list_filter = ["genre", "release_date"]

    # 사용자 정의 액션 추가
    actions = ["update_like_count"]  # 좋아요 수 갱신

    # 관리자 목록에 이미지를 표시하기 위한 메소드
    def cover_image(self, song):
        # format_html API는 장고 내에서 HTML 태그 문자열을 조합할 수 있는 가장 안전한 방법이다
        # 직접 HTML 태그 문자열을 조합하거나 mark_safe를 쓰지 않는게 좋다
        # format_html을 쓰고 조합에 필요한 인자도 format_html 인자로 넘기면 XSS 해킹 공격을 방어할 수 있다
        # 첫번째 인자에 f-string 문법으로 cover_url을 직접 조합하면 안되고 인자로 cover_url을 넘겨주어야 format_html이 의미가 있다
        return format_html('<img src="{}" style="width: 50px;"/>', song.cover_url)

    # 좋아요 수 업데이트 메소드
    # 인자 (self , 액션도 웹요청이기 떄문에 request, 선택된 레코드 쿼리셋)
    def update_like_count(self, request, queryset):
        # queryset에서 melon_uid 값을 리스트로 추출
        melon_uid_list = queryset.values_list("melon_uid", flat=True)

        # melonid 와 좋아요 수가 있는 dict 가져오기
        likes_dict = get_likes_dict(melon_uid_list)

        # song 별로 개별 UPDATE 쿼리
        # for song in queryset:
        #     song.like_count = likes_dict[song.melon_uid]
        #     song.save() # 개별 UPDATE 쿼리

        # 일괄 UPDATE 쿼리
        changed_count = 0
        for song in queryset:
            if song.like_count != likes_dict.get(song.melon_uid):
                song.like_count = likes_dict.get(song.melon_uid)
                changed_count += 1
        Song.objects.bulk_update(queryset, fields=["like_count"])

        # 장고의 message 프레임워크 사용하여 메시지 남기기
        self.message_user(request, message=f"{changed_count} 곡의 좋아요 갱신 완료")


# 모델 클래스 등록
# admin.site.register(Song, SongAdmin) -> @admin.register(Song) 으로 대체 가능
