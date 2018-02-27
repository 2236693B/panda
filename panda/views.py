from django.http import HttpResponse
<<<<<<< Updated upstream
from django.shortcuts import render


def index(request):

    context_dict = {}


    #return render(request, 'panda/index.html', context=context_dict)
    return HttpResponse("Hello, world") #Handy test to ensure pyrthon anywhere still working. Remove once render is probably handled
=======

def index(request):
    return HttpResponse("Hello, world")

def detail(request, game_id):
    return HttpResponse("You're looking at game%s." % game_id)

>>>>>>> Stashed changes
