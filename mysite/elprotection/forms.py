from django import forms
from .models import Employ, Position, Company, Admission, Protocol


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


class EmployForm(forms.ModelForm):
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
        fields = ['status', 'employ', 'admission', 'start', 'numbers', 'end']
