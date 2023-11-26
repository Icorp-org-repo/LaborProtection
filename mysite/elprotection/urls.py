from django.urls import path
from . import views

app_name = 'elprotection'

urlpatterns = [
    path('', views.protocol_list, name='index'),
    path('protocols/', views.protocol_list, name='protocols'),
    path('company/', views.company_list, name='list_company')
]
