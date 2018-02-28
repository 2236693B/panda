from django.shortcuts import render
#from django.http import HttpResponse
from .models import Game

def index(request):

    context_dict = {}

    game_list = Game.objects.order_by('-rating')[:5]

    context_dict = {'games': game_list}

    response = render(request, 'panda/index.html', context_dict)

    return response


