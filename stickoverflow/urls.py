from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'stickoverflow'

urlpatterns = [
	path('', views.IndexView.as_view(), name = 'index'),
	#

	path('logout', auth_views.LogoutView, {'next_page' : '/'}),
    path('login', auth_views.LoginView, {'template_name' : 'registration/login.html'}),    
]