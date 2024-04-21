from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib import messages

def index(request: HttpRequest):
    messages.debug(request=request, message="디버그 메시지")
    messages.info(request=request, message="정보 메시지")
    messages.success(request=request, message="성공 메시지")
    messages.warning(request=request, message="경고 메시지")
    messages.error(request=request, message="에러 메시지")
    return render(request=request, template_name='core/index.html')

