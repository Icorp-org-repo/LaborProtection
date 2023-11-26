from .models import Protocol
from django.shortcuts import render, get_object_or_404  # , redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView
# Create your views here.


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


