from django.urls import path
from . import views

app_name = 'elprotection'

urlpatterns = [
    path('', views.protocol_list, name='protocol_list')
]
