from django.shortcuts import render
from django.template.loader import render_to_string

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
            msg = render_to_string("account/msg.html",
                                   {'new_user': new_user, 'company_name': cd['company_name'],
                                    'position': cd['position'], 'category': cd['category'],
                                    'surname': cd['surname']})
            mail_admins(subject, msg, html_message=msg)

            messages.success(request, "Заявка оформлена прошу вас ожидать ответа на указанную почту")
            return render(request, 'account/register.html', {'user_form': user_form})

    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})
