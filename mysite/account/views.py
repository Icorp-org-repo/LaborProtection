from django.shortcuts import render
from .forms import UserRegistrationForm
from django.core.mail import send_mail, mail_admins
from django.contrib import messages
# Create your views here.
# mail_admins - для отправки сообщение Администраторам Сайта


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            cd = user_form.cleaned_data
            subject = f"{new_user.username} регистрация"
            message = (f"Name:{new_user.username} Почта: {new_user.email}\n Компания {cd['company_name']} Должность {cd['position']}"
                       f"\n{cd['position']} category: {cd['category']}\n"
                       f"{new_user.last_name} {new_user.first_name} {cd['surname']}")
            send_mail(subject, message, 'djangofortest777@gmail.com', ['elzig3012@gmail.com'])
            messages.success(request, "Заявка оформлена прошу вас ожидать ответа на указанную почту")
            return render(request, 'account/register.html', {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})
