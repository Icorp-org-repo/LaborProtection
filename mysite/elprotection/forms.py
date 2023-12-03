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
        fields = ['username', 'first_name', 'last_name', 'email']


class EmployCreateForm(forms.ModelForm):
    position = forms.ModelChoiceField(label="Должность",queryset=Position.objects.all(), required=True)
    boss = forms.ModelChoiceField(label="Начальник", queryset=Employ.objects.all(), required=False)

    class Meta:
        model = Employ
        fields = ['number', 'surname']

    def __init__(self, *args, positions=None, bosses=None,  **kwargs, ):
        super().__init__(*args, **kwargs)
        if not (positions is None):
            self.fields["position"].queryset = positions
            self.fields['boss'].queryset = bosses

    def clean_position(self):
        cd = self.cleaned_data
        if (cd['position'] is None) or (not cd['position']):
            raise forms.ValidationError("Должность обезательное поля")
        return cd['position']




class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['number', 'title', 'body', 'knowledge', 'type']


class ProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ['status', 'employ', 'admission', 'start', 'number', 'end']
