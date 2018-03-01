from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect#, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from panda.forms import UserForm, PlayerProfileForm, GameRatingForm, GameCommentForm , PlayerRatingForm

from .models import Game, Player,GameRating, Comment, PlayerRating
from django.contrib.auth.models import User


def index(request):

    context_dict = {}

    game_list = Game.objects.order_by('-rating')[:5]
    player_list =Player.objects.order_by('-rating')[:5]

    context_dict = {'games': game_list, 'players' : player_list}

    response = render(request, 'panda/index.html', context_dict)

    return response

def about(request):

    context_dict = { }

    return render(request, 'panda/about.html', context=context_dict)

def games(request):

    context_dict = {}

    game_list = Game.objects.order_by('-catergory')

    context_dict = {'games': game_list}

    response = render(request, 'panda/games.html', context_dict)

    return response

def show_game(request, game_name_slug):

    context_dict = {}

    try:
        game = Game.objects.get(slug = game_name_slug)
        context_dict['game'] = game

    except Game.DoesNotExist:
        context_dict['game'] = None

    return render(request, 'panda/game.html', context_dict)

@login_required
def make_game_rating(request,game_name_slug):

    name = request.user.username
    user = User.objects.get(username = name)
    player = Player.objects.get(user = user)

    try:
        game = Game.objects.get(slug= game_name_slug)

    except Game.DoesNotExist:
       game = None

    try:
        rating = GameRating.objects.get(player = player, rated = game)
        value = rating.value


    except GameRating.DoesNotExist:
       value = 'unrated'


    form = GameRatingForm()

    if request.method == 'POST':
        form = GameRatingForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            player.make_game_rating(game, data['value'])

            return show_game(request, game_name_slug)

        else:

            print(form.errors)

    context_dict = {'form':form, 'game':game, 'value': value}

    return render(request, 'panda/game_rating.html', context_dict)

@login_required
def make_game_comment(request,game_name_slug):

    name = request.user.username
    user = User.objects.get(username = name)
    player = Player.objects.get(user = user)

    try:
        game = Game.objects.get(slug= game_name_slug)

    except Game.DoesNotExist:
       game = None

    form = GameCommentForm()

    if request.method == 'POST':
        form = GameCommentForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            c = Comment.objects.create(player=player, comment = data['value'])
            c.save()
            game.comments.add(c)

            return show_game(request, game_name_slug)

        else:

            print(form.errors)

    context_dict = {'form':form, 'game':game}

    return render(request, 'panda/game_comment.html', context_dict)


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                err_message = "Your Panda account is disabled."
                return render(request, 'panda/login.html', {'err_message': err_message})

        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            err_message = "Invalid login details supplied."
            return render(request, 'panda/login.html', {'err_message': err_message})

    else:
        err_message = ''
        return render(request, 'panda/login.html', {'err_message': err_message})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def sign_up(request):
    registered = False
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = PlayerProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:

                profile.picture = request.FILES['picture']

            profile.save()

            registered=True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = PlayerProfileForm()

    return render(request, 'panda/sign_up.html', {'user_form': user_form, 'profile_form':profile_form, 'registered': registered})

@login_required
def players(request):

    context_dict = {}

    player_list = Player.objects.order_by('-id')

    context_dict = {'players': player_list}

    response = render(request, 'panda/players.html', context_dict)

    return response

@login_required
def show_player(request, player_name_slug):

    context_dict = {}

    try:
        player = Player.objects.get(slug = player_name_slug)
        context_dict['player'] = player

    except Game.DoesNotExist:
        context_dict['player'] = None

    return render(request, 'panda/player.html', context_dict)

@login_required
def make_player_rating(request,player_name_slug):

    warning = False

    name = request.user.username
    user = User.objects.get(username = name)
    rating_player = Player.objects.get(user = user)

    try:
        player = Player.objects.get(slug=player_name_slug)

    except Player.DoesNotExist:
       player = None

    if player == rating_player:
        player = None
        warning = True

    try:
        rating = PlayerRating.objects.get(player=rating_player, rated_player =player)
        value = rating.value


    except PlayerRating.DoesNotExist:
       value = 'unrated'


    form = PlayerRatingForm()

    if request.method == 'POST':
        form = PlayerRatingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            rating_player.make_player_rating(player, data['value'])

            return show_player(request, player_name_slug)

        else:

            print(form.errors)

    context_dict = {'form':form, 'player':player, 'value': value, 'warning':warning}

    return render(request, 'panda/player_rating.html', context_dict)

@login_required
def show_profile(request):

    context_dict = {}
    name = request.user.username
    user = User.objects.get(username = name)
    player = Player.objects.get(user = user)

    context_dict['player'] = player

    return render(request, 'panda/my_profile.html', context_dict)






