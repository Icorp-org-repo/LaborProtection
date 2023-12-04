from .models import Protocol, Employ, Position
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404  # , redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from .forms import LoginForm, EmployCreateForm, UserCreateForm, ProtocolCreateForm


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


@login_required
def show_protocols(request):
    is_admin = request.user.is_superuser
    if is_admin:
        protocols = Protocol.objects.all()
        messages.warning(request, "Вы SuperAdmin можете смотреть в адмн. понели")
    else:
        employ = Employ.objects.get(user=request.user)
        if employ.is_administrator:
            protocols = Protocol.objects.filter(employ__position__company=employ.position.company)
            is_admin = True
        else:
            protocols = Protocol.objects.filter(employ__boss=employ)

    return render(request,
                  'elprotection/protocol/list.html',
                  {
                      'protocols': protocols,
                      'active': 'Журнал',
                      'is_admin_company': is_admin
                  })

@login_required
def create_protocol(request):
    is_admin = request.user.is_superuser
    template_name = 'elprotection/protocol/create.html'
    if is_admin:
        messages.warning(request, "Вы SuperAdmin вам необходимо рабтать через Админ Панел")
        return redirect('/admin/')
    employ = Employ.objects.get(user=request.user)
    if not employ.is_administrator:
        messages.error(request, "У вас нет доступа обратитесь к администратору")
        return_path = request.META.get('HTTP_REFERER', '/')
        return redirect(return_path)
    my_company = employ.position.company
    employs = Employ.objects.filter(position__company=my_company)
    if request.method == "POST":
        form = ProtocolCreateForm(request.POST, employs=employs)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
    else:
        form = ProtocolCreateForm(employs=employs)
    return render(request,
                  template_name,
                  {
                      'form': form,
                      'active': 'Журнал',
                  })


@login_required
def create_employ(request):
    if request.user.is_superuser:
        messages.error(request,"Вы Админ")
        return redirect('/admin/elprotection/employ/add/')
    employ = Employ.objects.get(user=request.user)
    my_company = employ.position.company
    positions = Position.objects.filter(company=my_company)
    bosses = Employ.objects.filter(position__company=my_company)
    if request.method == "POST":
        user_form = UserCreateForm(request.POST,)
        profile_form = EmployCreateForm(request.POST,positions=positions, bosses=bosses)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_employ = profile_form.save(commit=False)
            password = User.objects.make_random_password()
            print(password)
            new_user.set_password(password)
            new_user.save()
            new_employ.user = new_user
            new_employ.position = profile_form.cleaned_data['position']
            new_employ.boss = profile_form.cleaned_data['boss']
            new_employ.save()
    else:
        user_form = UserCreateForm()
        profile_form = EmployCreateForm(positions=positions, bosses=bosses)

    return render(request,
                  'elprotection/employ/create.html',
                  {
                      'user_form': user_form,
                      'profile_form': profile_form,
                      'active': 'Сотрудники',
                  })


@login_required
def show_employ(request):
    is_admin = request.user.is_superuser
    if is_admin:
        return redirect('/admin/')
    employ = Employ.objects.get(user=request.user)
    return render(request,
                  'elprotection/employ/account.html',
                  {
                      'active': 'Личный кабинет',
                      'employ': employ,
                  })


@login_required
def show_employs(request):
    is_admin = request.user.is_superuser
    template_name = 'elprotection/employ/list.html'
    if is_admin:
        employs = Employ.objects.all()
    else:
        employ = Employ.objects.get(user=request.user)
        if employ.is_administrator:
            employs = Employ.objects.filter(position__company=employ.position.company)
            is_admin = True
        else:
            employs = Employ.objects.filter(boss=employ)

    return render(request,
                  template_name,
                  {
                      'active': 'Сотрудники',
                      'employs': employs,
                      'is_admin': is_admin,
                  })




# Этот список только для администратора сайта
@login_required
def company_list(request):
    protocols = Protocol.objects.all()
    return render(request,
                  'elprotection/protocol/list.html',
                  {
                      'protocols': protocols,
                      'active': 'Предприятии',
                  })