from django.shortcuts import render

# Create your views here.
from django.core.files.storage import FileSystemStorage

# file_upload part
def upload(request):
	context = {}
	user_id = "test"
	fs = FileSystemStorage()
	if request.method == 'POST':
		if request.FILES['document']:
			uploaded_file = request.FILES['document']
			name = fs.save(user_id + '/' + uploaded_file.name, uploaded_file)

	dir_list, file_list = fs.listdir(user_id + '/')
	context['url'] = file_list

	return render(request, 'stickoverflow/upload.html', context)

from django.views.generic.edit import CreateView, View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import CreateUserForm, LoginForm
from .models import User

# 회원가입 뷰
class CreateUserView(CreateView):
	def get(self, request, *args, **kwargs):
		form = CreateUserForm()
		context = {'form': form}
		return render(request, 'registration/signup.html', context)

	def post(self, request, *args, **kwargs):
		form = CreateUserForm(data = request.POST)
		if form.is_valid():
			user = form.save()
			user.save()
			return HttpResponseRedirect(reverse_lazy('create_user_done'))

		return render(request, 'registration/signup.html', {'form': form})

class LoginView(View):
	def get(self, request, *args, **kwargs):
		form = LoginForm()
		context = {'form': form}
		return render(request, 'registration/login.html', context)

	def post(self, request, *args, **kwargs):
		form = LoginForm(data = request.POST)
		if form.is_valid():
			self.check_login(form.cleaned_data)
			form = LoginForm()
			return render(request, 'registration/login.html', {'form': form})
		return render(request, 'registration/login.html', {'form': form})
	def check_login(self, valid_data):
		check = User.objects.filter(user_id__iexact = valid_data['user_id'])[0].check_password(valid_data['password'])
		print(check)


from django.views.generic.base import TemplateView

class RegisteredView(TemplateView):
    template_name = 'registration/signup_done.html'

class IndexView(TemplateView):
	template_name = 'stickoverflow/index.html'
class AboutUs(TemplateView):
	template_name = 'stickoverflow/aboutus.html'
class Result_View(TemplateView):
	template_name = 'stickoverflow/result_view.html'
