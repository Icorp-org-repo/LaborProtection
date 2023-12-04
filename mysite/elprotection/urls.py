from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'elprotection'

urlpatterns = [
    path('', views.show_employ, name='employ'),
    path('protocols/', views.show_protocols, name='protocols'),
    path('company/', views.company_list, name='list_company'),
    path('create_user/', views.create_employ, name='create_employ'),
    path('employs/', views.show_employs, name='list_employ'),
    path('create_protocol/', views.create_protocol, name='create_protocol'),
    path('create_position/', views.create_position, name='create_position'),
    path('employs/<slug:employ_slug>/edit/', views.edit_employ, name='edit_employ')
   # path('employs/', views.)
]
