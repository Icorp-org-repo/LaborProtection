from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    Category = [
        ('WO', "Рабочий"),
        ('MG', 'Руководитель'),
        ('SP', 'Специалист'),
    ]
    surname = forms.CharField(label='Отчество',required=False)
    company_name = forms.CharField(label="Название Компании", required=True, max_length=256)
    position = forms.CharField(label="Должность", required=True, max_length=256)
    category = forms.ChoiceField(label="Категория должности",choices=Category)

    class Meta:
        model = User
        fields = ['username', 'last_name','first_name', 'email']
