from django.http import HttpResponse 
from django.shortcuts import render


def index(request): 

    context_dict = {}


    return render(request, 'rango/index.html', context=context_dict)
