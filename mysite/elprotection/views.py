from .models import Protocol
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404  # , redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from .forms import LoginForm
# Create your views here.


def user_login(request):
    template = "elprotection/login.html"
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Проверка учетных данных пользователя
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Аутентификация прошла успешно')
                else:
                    return HttpResponse('Учетная запись заблокирована')
            else:
                return HttpResponse("Не верно указан логин")
    else:
        form = LoginForm()
    content = {'form': form}
    return render(request,
                  template,
                  content)


@login_required()
def protocol_list(request):
    protocols = Protocol.objects.all()
    return render(request,
                  'elprotection/protocol/list.html',
                  {
                      'protocols': protocols,
                      'active': 'Журнал',
                  })


def company_list(request):
    protocols = Protocol.objects.all()
    return render(request,
                  'elprotection/protocol/list.html',
                  {
                      'protocols': protocols,
                      'active': 'Предприятии',
                  })


