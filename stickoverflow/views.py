from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView


# 회원가입을 위한 import문 들
# from django.contrib.auth.forms import UserCreationForm  >>  장고의 기본 회원가입 폼 (ID, PW만 확인한다 - 뒤에서 이메일 추가 커스터미아징 예정)
from django.views.generic.edit import CreateView # 오브젝트를 생성하는 뷰 (form 혹은 model과 연결되서 새로운 데이터를 넣을 때 CreateView - generic view를 사용)
from .forms import CreateUserForm # 장고의 기본 회원가입 폼을 커스터마이징 한 폼
from django.urls import reverse_lazy # generic view에서는 reverse_lazy를 사용한다.


# file_upload part
from django.core.files.storage import FileSystemStorage

# file_upload part
def upload(request):
	context = {}
	if request.method == 'POST':
		uploaded_file = request.FILES['document']
		fs = FileSystemStorage() # 같은 파일일 경우 알아서 안 덮어쓰게 처리해줌.
		name = fs.save(uploaded_file.name, uploaded_file)
		context['url'] = fs.url(name)		
	return render(request, 'stickoverflow/upload.html', context) # template(기본값)의 stickoverflow안의 upload.html을 찾아감	


# CBV (Class Based View 작성!)
class CreateUserView(CreateView): # generic view중에 CreateView를 상속받는다.
    template_name = 'registration/signup.html' # 템플릿은?
    form_class =  CreateUserForm # 푸슨 폼 사용? >> 내장 회원가입 폼을 커스터마지징 한 것을 사용하는 경우
    # form_class = UserCreationForm >> 내장 회원가입 폼 사용하는 경우
    success_url = reverse_lazy('create_user_done') # 성공하면 어디로?

class RegisteredView(TemplateView): # generic view중에 TemplateView를 상속받는다.
    template_name = 'registration/signup_done.html' # 템플릿은?

class IndexView(TemplateView):
	template_name = 'stickoverflow/index.html'