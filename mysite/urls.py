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
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 메인 페이지
    path('', stickoverflow_views.IndexView.as_view(), name = 'index'),

    # 로그인
    path('accounts/login/', stickoverflow_views.LoginView.as_view(), name = 'login'),

    # 회원가입
    path('accounts/signup/', stickoverflow_views.CreateUserView.as_view(), name = 'signup'),
    path('accounts/signup/done/', stickoverflow_views.RegisteredView.as_view(), name = 'create_user_done'),

    path('accounts/logout/', stickoverflow_views.LogoutView.as_view(), name = 'logout'),

    # 업로드
    path('upload/', stickoverflow_views.UploadView.as_view(), name = 'upload'),

    # Product 추가
    path('aboutus/', stickoverflow_views.AboutUs.as_view(), name = 'aboutus'),
    path('result_select_view/', stickoverflow_views.ResultSelectView.as_view(), name = 'result_select_view'),
    path('result_view/', stickoverflow_views.ResultView.as_view(), name = 'result_view'),

]

# file_upload part
# Serving media files on local machine
if settings.DEBUG: # only during development
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
