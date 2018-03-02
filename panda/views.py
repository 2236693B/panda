from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect#, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from panda.forms import UserForm, PlayerProfileForm, GameRatingForm, GameCommentForm , PlayerRatingForm, GameRegisterForm, StudioProfileForm

from .models import Game, Player,GameRating, Comment, PlayerRating, GameStudio
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
    played = False
    player = False

    context_dict = {}


    try:
        game = Game.objects.get(slug = game_name_slug)
        context_dict['game'] = game

    except Game.DoesNotExist:
        context_dict['game'] = None

    if request.user.is_authenticated():
        if game.players.filter(user=request.user).exists():
            played = True
        if Player.objects.filter(user=request.user).exists():
            player = True

    context_dict['played'] = played
    context_dict['player'] = player



    return render(request, 'panda/game.html', context_dict)

@login_required
def make_game_rating(request,game_name_slug):
    studio_warning = False
    name = request.user.username
    user = User.objects.get(username = name)

    try:
        game = Game.objects.get(slug= game_name_slug)

    except Game.DoesNotExist:
       game = None

    try:
         player = Player.objects.get(user = user)

    except Player.DoesNotExist:
       studio_warning = True
       game = None
       player = None

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

    context_dict = {'form':form, 'game':game, 'value': value, 'studio_warning': studio_warning,'return':game_name_slug}

    return render(request, 'panda/game_rating.html', context_dict)

@login_required
def make_game_comment(request,game_name_slug):
    studio_warning = False
    name = request.user.username
    user = User.objects.get(username = name)

    try:
        game = Game.objects.get(slug= game_name_slug)

    except Game.DoesNotExist:
       game = None

    try:
         player = Player.objects.get(user = user)

    except Player.DoesNotExist:
       studio_warning = True
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

    context_dict = {'form':form, 'game':game, 'studio_warning':studio_warning, 'return':game_name_slug}

    return render(request, 'panda/game_comment.html', context_dict)

@login_required
def add_player(request, game_name_slug):
    context_dict = {}

    try:
        game = Game.objects.get(slug = game_name_slug)
        context_dict['game'] = game

        if request.user.is_authenticated():
            if not game.players.filter(user=request.user).exists():

                try:
                    player = Player.objects.get(user=request.user)
                    game.players.add(player)

                except Player.DoesNotExist:
                    player = None


    except Game.DoesNotExist:
        context_dict['game'] = None

    return show_game(request, game_name_slug)

@login_required
def remove_player(request, game_name_slug):
    context_dict = {}

    try:
        game = Game.objects.get(slug = game_name_slug)
        context_dict['game'] = game

        if request.user.is_authenticated():
            if game.players.filter(user=request.user).exists():
                try:
                    player = Player.objects.get(user=request.user)
                    game.players.remove(player)

                except Player.DoesNotExist:
                    player = None


    except Game.DoesNotExist:
        context_dict['game'] = None

    return show_game(request, game_name_slug)


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

    except Player.DoesNotExist:
        context_dict['player'] = None

    return render(request, 'panda/player.html', context_dict)

@login_required
def make_player_rating(request,player_name_slug):
    studio_warning = False
    player_warning = False

    name = request.user.username
    user = User.objects.get(username = name)

    try:
        player = Player.objects.get(slug=player_name_slug)

    except Player.DoesNotExist:
       player = None

    try:
         rating_player = Player.objects.get(user = user)

    except Player.DoesNotExist:
       studio_warning = True
       player = None
       rating_player = None

    if player == rating_player and rating_player != None:
        player = None
        player_warning = True

    try:
        rating = PlayerRating.objects.get(player=rating_player, rated_player=player)
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

    context_dict = {'form':form, 'player':player, 'value': value, 'player_warning':player_warning, 'studio_warning':studio_warning, 'return':player_name_slug}

    return render(request, 'panda/player_rating.html', context_dict)

@login_required
def show_profile(request):

    context_dict = {}
    name = request.user.username
    user = User.objects.get(username = name)
    player = None

    try:
        player = Player.objects.get(user = user)
        context_dict['player'] = player
        context_dict['games'] = player.game_set.all()
        return render(request, 'panda/my_profile_player.html', context_dict)

    except Player.DoesNotExist:
        studio = GameStudio.objects.get(user = user)
        context_dict['studio'] = studio
        context_dict['games'] = Game.objects.filter(studio=studio)
        return render(request, 'panda/my_profile_studio.html', context_dict)


@login_required
def register_game(request):

    name = request.user.username
    user = User.objects.get(username = name)

    try:
       studio = GameStudio.objects.get(user=user)

    except GameStudio.DoesNotExist:
      studio = None

    form = GameRegisterForm()

    if request.method == 'POST':
        form = GameRegisterForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.studio = studio

            game.save()

            return show_profile(request)

        else:

            print(form.errors)

    context_dict = {'form':form, 'studio':studio}

    return render(request, 'panda/register_game.html', context_dict)

@login_required
def edit_player_profile(request):
    try:
        player = Player.objects.get(user=request.user)

    except Player.DoesNotExist:
       player = None

    form = PlayerProfileForm( {'Bio': player.Bio, 'Steam': player.Steam, 'PSN' : player.PSN, 'Xbox': player.Xbox, 'Nintendo':player.Nintendo, 'picture':player.picture})

    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save(commit=True)
            return show_profile(request)
        else:
            print(form.errors)

    return render(request, 'panda/edit_player_profile.html', {'player': player, 'form': form})

@login_required
def edit_studio_profile(request):

    form = None

    try:
       studio = GameStudio.objects.get(user=request.user)
       form = StudioProfileForm( {'name':studio.name})

    except GameStudio.DoesNotExist:
       studio = None

    if request.method == 'POST':
        form = StudioProfileForm(request.POST, request.FILES, instance=studio)
        if form.is_valid():
            form.save(commit=True)
            return show_profile(request)
        else:
                err_message = "Studio name already in use"
                return render(request, 'panda//edit_studio_profile.html',{'studio': studio, 'form': form, 'err_message':err_message})

    return render(request, 'panda/edit_studio_profile.html', {'studio': studio, 'form': form,})











