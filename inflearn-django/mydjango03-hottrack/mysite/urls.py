from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

# from hottrack.views import index

urlpatterns = [
    path(route="admin/", view=admin.site.urls),
    path(route="hottrack/", view=include("hottrack.urls")),
    path(route="", view=lambda request: redirect("/hottrack/")),
    # path(route="hottrack/", view=index),
]

# settings 파일이 아닌 다른 파일에서 settings 설정값을 참조할 때
# from mysite import settings를 하면 안되고
# settings.py 위치에 상관없이 from django.conf import settings 를 해아한다
# 왜냐하면 장고에는 140여개의 기본 설정이 있고, 우리 프로젝트의 mysite/settings.py는
# 이 기본 설정을 재정의하는 역할이기 떄문에 두 설정을 합쳐야 한다(그 역할을 from django.conf import settings 여기서 해준다)

if settings.DEBUG:
    urlpatterns += [
        path(route="__debug__/", view=include("debug_toolbar.urls")),
    ]
