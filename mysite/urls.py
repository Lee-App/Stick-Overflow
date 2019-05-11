"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from stickoverflow import views as stickoverflow_views

# file_upload part
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', stickoverflow_views.IndexView.as_view()),
    path('stickoverflow', include('stickoverflow.urls')),

    # 수정이 필요할지도 모르겠다.
    # 계속해서 기존의 url형식을 path로 바꿔줘야 하니...
    path('', include('django.contrib.auth.urls')),

    # 회원가입
    # 회원가입 url이 따로 장고의 auth.urls에 없어서 구현해줘야한다.
    path('accounts/signup', stickoverflow_views.CreateUserView.as_view(), name = 'signup'),
    path('accounts/login/done', stickoverflow_views.RegisteredView.as_view(), name = 'create_user_done'),
    path('upload/', stickoverflow_views.upload, name = 'upload'), # views.py의 upload를 찾아감.
]

# file_upload part
# Serving media files on local machine
if settings.DEBUG: # only during development
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)