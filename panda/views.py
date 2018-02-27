from django.http import HttpResponse
from django.shortcuts import render


def index(request):

    context_dict = {}


    #return render(request, 'panda/index.html', context=context_dict)
    return HttpResponse("Hello, world") #Handy test to ensure pyrthon anywhere still working. Remove once render is probably handled
