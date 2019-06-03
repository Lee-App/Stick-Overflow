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

from django.views.generic.edit import CreateView
from .forms import CreateUserForm

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
	success_url = reverse_lazy('create_user_done') # 성공하면 어디로?

	def post(self, request, *args, **kwargs):
		form = CreateUserForm(data = request.POST)

		if form.is_valid():
			check = self.is_sign_up_done(form.cleaned_data)

			if check:
				user = form.save()
				user.input_id = user.update_id = user.user_id
				user.input_ip = user.update_ip = self.get_client_ip(request)
				user.save()

				return HttpResponseRedirect(reverse_lazy('create_user_done'))

		return render(request, 'registration/signup.html', {'form': form})

	def is_sign_up_done(self, valid_data):
		rst = True

		# password != confirm_password
		if valid_data['password'] != valid_data['confirm_password']:
			rst = False

		# exists user id
		if User.objects.filter(user_id__iexact = valid_data['user_id']):
			rst = False

		return rst

	def get_client_ip(self, request):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		return ip

import os
import time
from django.views.generic.edit import View
from .forms import UploadForm
from .models import File

class UploadView(View):
	def get(self, request, *args, **kwargs):
		context = self.upload(request)
		return render(request, 'stickoverflow/upload.html', context)

	def post(self, request, *args, **kwargs):
		context = self.upload(request)
		return render(request, 'stickoverflow/upload.html', context)

	# file_upload part
	def upload(self, request):
		# print(File.objects.all().delete())
		fs = FileSystemStorage()
		form = UploadForm(data = request.POST)
		context = {'form': form }
		user_id = ''

		if "user" in request.session:
			user_id = request.session['user']

		if user_id and not fs.exists(user_id + '/'):
			mkdir(fs.path(user_id + '/'))

		if request.method == 'POST' and request.FILES['file']:
			# File Save
			uploaded_file = request.FILES['file']
			file_full_name = '{}/{}'.format(user_id, uploaded_file)
			real_name = fs.save(file_full_name, uploaded_file)
			# DB
			file_name = real_name[len(user_id) + 1:]
			file_path = '{}/'.format(user_id)
			file_description = request.POST['description']
			file = File(user_id = user_id, file_no = len(File.objects.all()), file_name = file_name, file_path = file_path, file_description = file_description)
			file.save()
			del request.FILES['file']

		files = File.objects.filter(user_id__iexact = user_id)

		if files:
			file_list = []

			for f in files:
				file_name = '{} <{}>'.format(f.file_name[:-4], f.file_no)
				file_type = f.file_name[-3:]
				file_desc = f.file_description
				file_no = f.file_no

				tmp = [file_name, file_type, file_desc, file_no]
				file_list.append(tmp)

			context['file_list'] = file_list


		return context

from .forms import LoginForm
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
				# Login Failed
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

from django.shortcuts import redirect
from .statistics_model import result, get_graph_data

class ResultViewTest(View):
	def get(self, request, *args, **kwargs):
		response = "<script>alert('잘못된 접근입니다!');window.history.back();</script>"
		return HttpResponse(response)

	def post(self, request, *args, **kwargs):
		fs = FileSystemStorage()
		user_id = ''

		if "user" in request.session:
			user_id = request.session['user']

		file_no = request.POST['file_no']
		file = File.objects.filter(file_no__iexact = file_no)
		file_full_path = file[0].file_path + file[0].file_name
		option = request.POST['option']

		if len(file) > 1:
			response = "<script>alert('잘못된 접근입니다!');window.history.back();</script>"
			return HttpResponse(response)

		real_path = fs.path(file_full_path)
		graph_data = result(real_path, option, x_label_col = '사용일자', y_label_col = '승차총승객수')
		graph_data = get_graph_data(graph_data, options = {'title' : file[0].file_name[:-4]})
		print(graph_data)
		context = {'graph_data' : graph_data}

		return render(request, 'stickoverflow/result_view_test.html', context)
