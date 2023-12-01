from django import forms
from .models import Employ, Position, Company, Admission, Protocol
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['title']


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'company', 'category']


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name',]

class EmployForm(forms.Form):
    number = forms.CharField(label="Табельный номер")
    second_name = forms.CharField(label="Фамилия")
    name = forms.CharField(label="Имя")
    surname = forms.CharField(label='Отчество')


    class Meta:
        model = Employ
        fields = ['number', 'second_name', 'name', 'surname', 'position', 'boss']


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['number', 'title', 'body', 'knowledge', 'type']


class ProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ['status', 'employ', 'admission', 'start', 'number', 'end']
