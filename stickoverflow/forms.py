from .models import User
from django import forms

# 회원가입 폼
class CreateUserForm(forms.ModelForm):
    user_id = forms.CharField(max_length = 50, label = 'id', required = True)
    password = forms.CharField(max_length = 50, label = 'password', widget = forms.PasswordInput, required = True)
    confirm_password = forms.CharField(max_length = 50, label = 'confirm password', widget = forms.PasswordInput, required = True)
    user_name = forms.CharField(max_length = 50, label = 'name', required = True)
    email = forms.EmailField(label = 'E-Mail', required = True)
    department = forms.CharField(max_length = 50, label = 'department')

    class Meta:
        model = User
        fields = ("user_id", "password", "confirm_password", "user_name", "email", "department")


class LoginForm(forms.Form):
    user_id = forms.CharField(max_length = 50, label = 'id', required = True)
    password = forms.CharField(max_length = 50, label = 'password', widget = forms.PasswordInput, required = True)


class UploadForm(forms.Form):
    file = forms.FileField()
    description = forms.CharField(max_length = 200, label = 'file description')
