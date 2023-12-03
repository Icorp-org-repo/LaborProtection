from .models import Protocol, Employ
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404  # , redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from .forms import LoginForm, EmployCreateForm, UserCreateForm
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

@login_required
def company_list(request):
    protocols = Protocol.objects.all()
    return render(request,
                  'elprotection/protocol/list.html',
                  {
                      'protocols': protocols,
                      'active': 'Предприятии',
                  })

@login_required
def create_employ(request):
    if request.method == "POST":
        user_form = UserCreateForm(request.POST, instance=request.user)
        profile_form = EmployCreateForm(request.POST, instance=request.user.employ)
        if user_form.is_valid() and profile_form.is_valid():
            pass
    else:
        user_form = UserCreateForm(instance=request.user)
        profile_form = EmployCreateForm(instance=request.user.employ)

    return render(request,
                  'elprotection/employ/create.html',
                  {
                      'user_form': user_form,
                      'profile_form': profile_form
                  })


@login_required
def show_employ(request):
    is_admin = request.user.is_superuser
    if is_admin:
        return redirect('/admin/')
    employ = Employ.objects.get(user=request.user)
    print(employ.user.last_name)
    return render(request,
                  'elprotection/employ/account.html',
                  {
                      'active': 'Личный кабинет',
                      'employ': employ,
                  })
