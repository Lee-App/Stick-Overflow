from django.shortcuts import render

# Create your views here.
from django.core.files.storage import FileSystemStorage
from os import mkdir
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy

from .models import User


from django.views.generic.edit import CreateView
from .forms import CreateUserForm

# 회원가입 뷰
class CreateUserView(CreateView):

	def get(self, request, *args, **kwargs):
		form = CreateUserForm()
		context = {'form': form}
		return render(request, 'registration/signup.html', context)

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

from django.views.generic.edit import View
from .forms import UploadForm

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
				fs.save(file_full_name, uploaded_file)
				# view_table
				size = fs.size(file_full_name)
				# DB
				file_name = uploaded_file
				file_path = MEDIA_URL + '/' + user_id + '/'
				file_description = form.cleaned_data['description']
				print(file_name, file_path, file_description)
				del request.FILES['file']

		if user_id:
			if not fs.exists(user_id + '/'):
				mkdir(fs.path(user_id + '/'))

			dir_list, file_list = fs.listdir(user_id + '/')
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

def file_list(request):
	path = "/stick_overflow/media" # 로컬 경로여서 이 부분에서 못 불러올 수 있습니다.
	flist = os.listdir(path)
	return render_to_resposnse('upload.html', {'file_list': flist})
