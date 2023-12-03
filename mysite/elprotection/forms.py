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
        fields = ['first_name', 'last_name', 'email']


class EmployCreateForm(forms.Form):

    class Meta:
        model = Employ
        fields = ['number', 'surname', 'position', 'boss']


class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['number', 'title', 'body', 'knowledge', 'type']


class ProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ['status', 'employ', 'admission', 'start', 'number', 'end']
