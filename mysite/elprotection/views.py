from .models import Protocol, Employ, Position
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404  # , redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.template.loader import render_to_string
from .forms import LoginForm, EmployCreateForm, UserCreateForm, ProtocolCreateForm, PositionCreateForm
from .forms import UserEditForm, EmployEditForm


# Create your views here.
admin_email = "djangofortest777@gmail.com"

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
                      'is_admin': is_admin
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
            return redirect('elprotection:protocols', permanent=True)
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
    if not employ.is_administrator:
        messages.error(request, "У вас нет доступа обратитесь к администратору")
        return_path = request.META.get('HTTP_REFERER', '/')
        return redirect(return_path)
    if request.method == "POST":
        user_form = UserCreateForm(request.POST,)
        profile_form = EmployCreateForm(request.POST,positions=positions, bosses=bosses)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_employ = profile_form.save(commit=False)
            password = User.objects.make_random_password()
            msg = render_to_string("elprotection/employ/msg_create.html",
                             {'username': new_user.username, 'password':password})
            new_user.set_password(password)
            new_employ.user = new_user
            new_employ.position = profile_form.cleaned_data['position']
            new_employ.boss = profile_form.cleaned_data['boss']
            new_user.save()
            new_employ.save()
            send_mail('Создали учетную запись', msg, admin_email, [new_user.email], html_message=msg)
            return redirect('elprotection:list_employ', permanent=True)
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
    protocols = Protocol.objects.filter(employ=employ)
    return render(request,
                  'elprotection/employ/account.html',
                  {
                      'active': 'Личный кабинет',
                      'employ': employ,
                      'protocols':protocols,
                  })


@login_required
def employ(request):
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
def edit_employ(request, employ_slug):
    is_admin = request.user.is_superuser
    if is_admin:
        return redirect(f'/admin/elprotection/employ/{employ_slug}/change/')
    employ = Employ.objects.get(user=request.user)
    target_employ = Employ.objects.get(slug=employ_slug)
    if employ != target_employ:
            if not (employ.is_administrator):
                messages.error(request, "У вас нет доступа обратитесь к администратору")
                return_path = request.META.get('HTTP_REFERER', '/')
                return redirect(return_path)
            elif employ.position.company != target_employ.position.company:
                messages.error(request, "У вас нет доступа обратитесь к администратору")
                return_path = request.META.get('HTTP_REFERER', '/')
                return redirect(return_path)
    if request.method == 'POST':
        user_form = UserEditForm(instance=target_employ.user, data=request.POST)
        employ_form = EmployEditForm(instance=request.user.employ, data=request.Post)
        if user_form.is_valid() and employ_form.is_valid():
            user_form.save()
            employ_form.save()
            return redirect('elprotection:list_employ', permanent=True)
    else:
        user_form = UserEditForm(instance=target_employ.user)
        employ_form = EmployEditForm(instance=target_employ)
    return render(request,
                  'elprotection/employ/edit.html',
                  {
                      'active': 'Сотрудники',
                      'user_form': user_form,
                      'employ_form': employ_form
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


@login_required
def create_position(request):
    if request.user.is_superuser:
        messages.error(request, "Вы Админ")
        return redirect('/admin/elprotection/position/add/')
    employ = Employ.objects.get(user=request.user)
    if not employ.is_administrator:
        messages.error(request, "У вас нет доступа обратитесь к администратору")
        return_path = request.META.get('HTTP_REFERER', '/')
        return redirect(return_path)
    my_company = employ.position.company
    if request.method == "POST":
        form = PositionCreateForm(request.POST)
        if form.is_valid():
            new_position = form.save(commit=False)
            new_position.company = my_company
            new_position.save()
        return redirect('elprotection:list_employ')
    else:
        form = PositionCreateForm()

    return render(request,
                  'elprotection/employ/create_position.html',
                  {
                      'form': form,
                      'active': 'Сотрудники',
                  })