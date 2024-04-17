from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# 타입을 지정하면 이상한 타입추론도 줄이고 보다 빠르고 정확하게 자동완성을 제공받을 수 있다
def index(request: HttpRequest) -> HttpResponse:  # view 함수의 반환 타입은 HttpResponse
    return render(
        request=request,
        template_name="hottrack/index.html",
    )
