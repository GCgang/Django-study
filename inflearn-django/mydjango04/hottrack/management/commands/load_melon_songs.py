# hottrack/management/commands/load_melon_songs.py

import json
from urllib.request import urlopen  # URL을 통해 원격 데이터에 접근할 수 있게 해준다
from django.core.management import BaseCommand
from hottrack.models import Song


class Command(BaseCommand):
    help = "Load songs from melon chart"

    def handle(self, *args, **options):
        melon_chart_url = "https://raw.githubusercontent.com/pyhub-kr/dump-data/main/melon/melon-20230910.json"
        # urlopen: URL을 인자로 받고, 그 URL에 해당하는 서버에 HTTP 요청을 보내고, 서버로부터의 응답을 받는 객체를 반환한다
        # read(): 해당 객체의 내용을 바이트 스트림으로 읽음
        # decode("utf-8"): 바이트 형식으로 받아온 데이터를 인코딩하여 문자열로 변환
        json_string = urlopen(melon_chart_url).read().decode("utf-8")

        # 외부 필드명을 그대로 쓰기보다, 내부적으로 사용하는 필드명으로 변경하고, 필요한 메서드를 추가합니다.
        # json.loads(json_string): json_string을 파이썬 딕셔너리로 반환
        # Song 인스턴스들은 아직 데이터베이스에 저장되지 않는다
        song_list = [Song.from_dict(song_dict) for song_dict in json.loads(json_string)]
        print("loaded song_list :", len(song_list))

        # Song 인스턴스들은 한 번에 INSERT 쿼리를 생성하여, INSERT 성능을 높인다
        Song.objects.bulk_create(
            song_list, batch_size=len(song_list), ignore_conflicts=True
        )

        total = Song.objects.all().count()
        print("saved song_list :", total)
