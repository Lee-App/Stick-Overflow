from django.shortcuts import render

# Create your views here.
from django.core.files.storage import FileSystemStorage
from os import mkdir
from django.views.generic.edit import CreateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import CreateUserForm, LoginForm, UploadForm
from .models import User

class UploadView(View):
	def get(self, request, *args, **kwargs):
		context = self.upload(request)
		return render(request, 'stickoverflow/upload.html', context)

	def post(self, request, *args, **kwargs):
		context = self.upload(request)
		return render(request, 'stickoverflow/upload.html', context)

	# file_upload part
	def upload(self, request):
		fs = FileSystemStorage()
		form = UploadForm()
		context = {'form': form }
		user_id = ''

		if "user" in request.session:
			user_id = request.session['user']

		if request.method == 'POST':
			if request.FILES['file']:
				uploaded_file = request.FILES['file']
				file_full_name = user_id + '/' + uploaded_file.name
				name = fs.save(file_full_name, uploaded_file)
				uploaded_file = ""

		if user_id:
			if not fs.exists(user_id + '/'):
				mkdir(fs.path(user_id + '/'))

			dir_list, file_list = fs.listdir(user_id + '/')
			context['file_list'] = file_list

		return context
from .forms import CreateUserForm #, LoginForm
from .models import User

import os

# 회원가입 뷰
class CreateUserView(CreateView):
	def get(self, request, *args, **kwargs):
		form = CreateUserForm()
		context = {'form': form}
		return render(request, 'registration/signup.html', context)


# CBV (Class Based View 작성!)
class CreateUserView(CreateView): # generic view중에 CreateView를 상속받는다.
	template_name = 'registration/signup.html' # 템플릿은?
	form_class =  CreateUserForm # 무슨 폼 사용? >> 내장 회원가입 폼을 커스터마이징 한 것을 사용하는 경우
    # form_class = UserCreationForm >> 내장 회원가입 폼 사용하는 경우
	success_url = reverse_lazy('create_user_done') # 성공하면 어디로?

	def post(self, request, *args, **kwargs):
		form = CreateUserForm(data = request.POST)
		if form.is_valid():
			user = form.save()
			user.save()
			return HttpResponseRedirect(reverse_lazy('create_user_done'))

		return render(request, 'registration/signup.html', {'form': form})

# 로그인 뷰
class LoginView(View):
	def get(self, request, *args, **kwargs):
		form = LoginForm()
		context = {'form': form}
		return render(request, 'registration/login.html', context)

	def post(self, request, *args, **kwargs):
		form = LoginForm(data = request.POST)
		if form.is_valid():
			is_user = self.check_login(form.cleaned_data)
			if is_user:
				# Login Success
				request.session["user"] = is_user.user_id
			else:
				form = LoginForm()
				return render(request, 'registration/login.html', {'form': form})

		return render(request, 'registration/login.html', {'form': form})

	def check_login(self, valid_data):
		user = User.objects.filter(user_id__iexact = valid_data['user_id'])
		check = False
		if user:
			check = user[0].check_password(valid_data['password'])

		if check:
			return user[0]
		else:
			return False

class LogoutView(View):
	def get(self, request, *args, **kwargs):
		self.logout(request)
		return render(request, 'registration/logged_out.html')

	def post(self, request, *args, **kwargs):
		self.logout(request)
		return render(request, 'registration/logged_out.html')

	def logout(self, request):
		request.session['user'] = ''
		request.session.modified = True

from django.views.generic.base import TemplateView

class RegisteredView(TemplateView):
    template_name = 'registration/signup_done.html'

class IndexView(TemplateView):
	template_name = 'stickoverflow/index.html'

class AboutUs(TemplateView):
	template_name = 'stickoverflow/aboutus.html'

class ResultView(TemplateView):
	template_name = 'stickoverflow/result_view.html'
class Result_View(TemplateView):
	template_name = 'stickoverflow/result_view.html'

def file_list(request):
	path = "/stick_overflow/media" # 로컬 경로여서 이 부분에서 못 불러올 수 있습니다.
	flist = os.listdir(path)
	return render_to_resposnse('upload.html', {'file_list': flist})
