from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'elprotection'

urlpatterns = [
    path('', views.protocol_list, name='protocols'),
    path('company/', views.company_list, name='list_company'),
]
