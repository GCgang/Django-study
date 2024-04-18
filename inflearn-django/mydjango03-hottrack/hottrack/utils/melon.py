import json
from typing import List, Dict
from urllib.parse import urlencode
from urllib.request import Request, urlopen

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
    ),
}


def get_likes_dict(melon_uid_list: List[str]) -> Dict[str, int]:
    url = "https://www.melon.com/commonlike/getSongLike.json"  # 멜론 좋아요 수를 가져오는 API
    # 멜론 API에 전달할 곡 ID들을 쿼리 문자열로 변환
    params = urlencode(
        {
            "contsIds": ",".join(melon_uid_list),
        }
    )
    url_with_params = url + "?" + params  # 전체 url 구성
    request = Request(url_with_params, headers=HEADERS)  # GET 요청 객체

    # 요청후 응답을 받아 파이썬 딕셔너리로 변환
    result = json.loads(urlopen(request).read())

    # 각 곡의 ID와 좋아요 수를 추츨하여 딕셔너리로 만듦
    likes_dict = {str(song["CONTSID"]): song["SUMMCNT"] for song in result["contsLike"]}

    return likes_dict
