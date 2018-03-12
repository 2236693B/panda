from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from panda.forms import UserForm, PlayerProfileForm, GameRatingForm, GameCommentForm , PlayerRatingForm, GameRegisterForm, StudioProfileForm, ReportingPlayerForm

from .models import Game, Player,GameRating, Comment, PlayerRating, GameStudio

import requests as r
import json

#View for Home page which features top 5 games and players
def index(request):
    context_dict = {}

    game_list = Game.objects.order_by('-rating')[:5]
    player_list =Player.objects.order_by('-rating')[:5]

    context_dict = {'games': game_list, 'players' : player_list}

    response = render(request, 'panda/index.html', context_dict)
    return response

#View for about page, which is static
def about(request):

    context_dict = { }

    return render(request, 'panda/about.html', context=context_dict)


#View for games page, returns games list sorted by catergory
def games(request):
    context_dict = {}

    no_cat = Game.objects.filter(catergory = 'NON')
    act_cat = Game.objects.filter(catergory ='ACT')
    adv_cat = Game.objects.filter(catergory ='ADV')
    rol_cat = Game.objects.filter(catergory ='ROL')
    mmo_cat = Game.objects.filter(catergory ='MMO')
    fps_cat = Game.objects.filter(catergory ='FPS')
    spo_cat = Game.objects.filter(catergory ='SPO')

    game_list = [no_cat, act_cat, adv_cat, rol_cat, mmo_cat, fps_cat, spo_cat, ]

    context_dict['games'] = game_list

    response = render(request, 'panda/games.html', context_dict)
    return response

def games_search(request):

    if request.method == 'POST':
        search = request.POST.get('search')
        game_list = Game.objects.filter(name__icontains=search)
        context_dict = {'results': game_list, 'search_request':search, "search":True}

        response = render(request, 'panda/games.html', context_dict)  # Return to game page after making rating
        return response

    return games(request)

#View for displaying indivdual game
def show_game(request, game_name_slug):
    played = False
    player = False
    owner = False

    context_dict = {}

    game = check_game(game_name_slug)
    context_dict['game'] = game

    #Steam API
    if game != None:
        if game.steam_id != None:
            try:
                new_request = "http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid=" + str(game.steam_id) + "&count=3&maxlength=300&format=json"
                news_response = r.get(new_request)
                news = news_response.json()
                news = news["appnews"]["newsitems"]

                world_players_request = "http://api.steampowered.com/ISteamUserStats/GetGlobalStatsForGame/v0001/?format=json&appid=" + str(17740) +"&count=1&name[0]=global.map.emp_isle"
                world_players_response = r.get( world_players_request)
                world_players =  world_players_response.json()
                world_players =  world_players["response"]["globalstats"]["global.map.emp_isle"]["total"]

                context_dict['news'] = news
                context_dict['world_players'] = str(world_players)

            except KeyError:
                context_dict['news'] = None
                context_dict['world_players'] = None



    #If user is logged in
    if request.user.is_authenticated():

        #Check if player object
        if Player.objects.filter(user=request.user).exists():
            player = True

            #Check if player plays game
            if game.players.filter(user=request.user).exists():
                played = True

        #If not user, check if user is owner
        elif game.studio.user == request.user:
            owner = True

    context_dict['played'] = played
    context_dict['player'] = player
    context_dict['owner'] = owner

    return render(request, 'panda/game.html', context_dict)

#View for handling making a rating on game
@login_required
def make_game_rating(request,game_name_slug):

    studio_warning, game, player = user_check(request, game_name_slug)

    #get current Player rating for game if it exists
    try:
        rating = GameRating.objects.get(player = player, rated = game)
        value = rating.value

    #Otherwise set it to unrated
    except GameRating.DoesNotExist:
       value = 'unrated'

    form = GameRatingForm()

    if request.method == 'POST':
        form = GameRatingForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            player.make_game_rating(game, data['value'])  #Helper function of Player model to make/edit game rating

            return show_game(request, game_name_slug) #Return to game page after making rating

        else:
            print(form.errors)

    context_dict = {'form':form, 'game':game, 'value': value, 'studio_warning': studio_warning,'return':game_name_slug}

    return render(request, 'panda/game_rating.html', context_dict)

#View for handling making a comment on game
@login_required
def make_game_comment(request,game_name_slug):

    studio_warning, game, player = user_check(request, game_name_slug)

    form = GameCommentForm()

    if request.method == 'POST':
        form = GameCommentForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            #Create new comment for current game
            c = Comment.objects.create(player=player, comment = data['comment'])
            c.save()
            game.comments.add(c)

            return show_game(request, game_name_slug) #Return to game page after making comment

        else:
            print(form.errors)

    context_dict = {'form':form, 'game':game, 'studio_warning':studio_warning, 'return':game_name_slug}

    return render(request, 'panda/game_comment.html', context_dict)

@login_required
def edit_game_comment(request, game_name_slug, comment_id):

    form = None
    owner = False

    player = check_player_user(request.user)
    #Retrieve comment from id

    game = check_game(game_name_slug)

    c = check_comment(comment_id)

    #If the player owns the commment, allow editing it
    if c!= None and c.player == player:
        owner = True
        form = GameCommentForm( {'comment':c.comment})

    if request.method == 'POST':
        form = GameCommentForm(request.POST, request.FILES, instance=c)
        if form.is_valid():
            form.save(commit=True)
            return show_game(request, game_name_slug)

    return render(request, 'panda/edit_comment.html', {'owner': owner, 'game': game, 'comment': c, 'form': form,})

#Delete players game comment
@login_required
def delete_game_comment(request,game_name_slug, comment_id):

    player = check_player_user(request.user)
    #Retrieve comment from id
    c = check_comment(comment_id)

    #If the player pwns the commment, delete it
    if c!= None and c.player == player:
        c.delete()

    return show_game(request, game_name_slug) #Return to game page after making comment

#View for adding player to game players list
@login_required
def add_player(request, game_name_slug):
    context_dict = {}

    game = check_game(game_name_slug)
    context_dict['game'] = game

    if request.user.is_authenticated():
        if not game.players.filter(user=request.user).exists():
                player = Player.objects.get(user=request.user)
                game.players.add(player)

    return show_game(request, game_name_slug)

#View for removing player to game players list
@login_required
def remove_player(request, game_name_slug):
    context_dict = {}

    game = check_game(game_name_slug)
    context_dict['game'] = game

    if request.user.is_authenticated():
        if game.players.filter(user=request.user).exists():
                player = Player.objects.get(user=request.user)
                game.players.remove(player)

    return show_game(request, game_name_slug)

#Generic user login in view
def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)

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

#Generic user logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

#Sign up view for player
def sign_up(request):
    
	registered = False
    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = PlayerProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) #Hash users password for safety
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

    return render(request, 'panda/sign_up.html', {'user_form': user_form, 'profile_form':profile_form, 'registered': registered, 'player': True})


	
#Sign up view for studio
def studio_sign_up(request):
    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = StudioProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered=True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = StudioProfileForm()

    return render(request, 'panda/sign_up.html', {'user_form': user_form, 'profile_form':profile_form, 'registered': registered, 'player':False})

#View to display players page, ordered by rating
@login_required
def players(request):

    context_dict = {}

    player_list = Player.objects.order_by('-rating')

    context_dict = {'players': player_list}

    response = render(request, 'panda/players.html', context_dict)

    return response

#View to show player page
@login_required
def show_player(request, player_name_slug):

    context_dict = {}

    player = check_player(player_name_slug)
    context_dict['player'] = player

    return render(request, 'panda/player.html', context_dict)

def player_search(request):

    if request.method == 'POST':
        search = request.POST.get('search')
        player_list = Player.objects.filter(user__username__icontains=search)
        context_dict = {'results': player_list, 'search_request':search, "search":True}

        response = render(request, 'panda/players.html', context_dict)  # Return to game page after making rating
        return response

    return players(request)

#View to make player rating
@login_required
def make_player_rating(request,player_name_slug):
    studio_warning = False
    player_warning = False

    player = check_player(player_name_slug)

    rating_player = check_player_user(request.user)

    #If studio trying to rate player
    if rating_player == None:
        studio_warning = True
        player = None

    #Check to make sure players not trying to rate themselves
    if player == rating_player and rating_player != None:
        player = None
        player_warning = True

    #Try to get player rating for current player if it exists
    try:
        rating = PlayerRating.objects.get(player=rating_player, rated_player=player)
        value = rating.value

    #Otherwise set it unrated
    except PlayerRating.DoesNotExist:
       value = 'unrated'

    form = PlayerRatingForm()

    if request.method == 'POST':
        form = PlayerRatingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            rating_player.make_player_rating(player, data['value'])  #Helper function in player to make/edit player ratings

            return show_player(request, player_name_slug)

        else:

            print(form.errors)

    context_dict = {'form':form, 'player':player, 'value': value, 'player_warning':player_warning, 'studio_warning':studio_warning, 'return':player_name_slug}

    return render(request, 'panda/player_rating.html', context_dict)

@login_required
def report_player(request, player_name_slug):

    player = check_player(player_name_slug)

    form = ReportingPlayerForm()

    if request.method == 'POST':
        form = ReportingPlayerForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.player = player

            report.save()

            return show_player(request, player_name_slug)

    context_dict = {'form': form, 'player': player}

    return render(request, 'panda/report.html', context_dict)


#Show studio or player's own profile
@login_required
def show_profile(request):

    context_dict = {}

    if not request.user.is_superuser:

        try:
            player = Player.objects.get(user = request.user)
            context_dict['player'] = player
            context_dict['games'] = player.game_set.all()
            return render(request, 'panda/my_profile_player.html', context_dict)

        except Player.DoesNotExist:
            studio = GameStudio.objects.get(user = request.user)
            context_dict['studio'] = studio
            context_dict['games'] = Game.objects.filter(studio=studio)
            return render(request, 'panda/my_profile_studio.html', context_dict)
    else:
        return HttpResponse("Please login in at the admin site <a href ='/admin/'>Here</a>")


#View to allow studio to register game
@login_required
def register_game(request):

    studio = check_studio_user(request.user)

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

    player = check_player_user(request.user)

    if player != None:
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

    studio = check_studio_user(request.user)

    if studio != None:
         form = StudioProfileForm( {'name':studio.name})

    if request.method == 'POST':
        form = StudioProfileForm(request.POST, request.FILES, instance=studio)
        if form.is_valid():
            form.save(commit=True)
            return show_profile(request)
        else:
                err_message = "Studio name already in use"
                return render(request, 'panda//edit_studio_profile.html',{'studio': studio, 'form': form, 'err_message':err_message})

    return render(request, 'panda/edit_studio_profile.html', {'studio': studio, 'form': form,})

@login_required
def edit_game_profile(request, game_name_slug):

    form = None
    edit = False

    try:
       game = Game.objects.get(slug = game_name_slug)
       form = GameRegisterForm( {'studio':game.studio, 'name':game.name, 'extract':game.extract, 'site':game.site,'date':game.date,'catergory':game.catergory,'picture':game.picture, 'Playstation':game.Playstation, 'Xbox':game.Xbox, 'PC':game.PC, 'Nintendo':game.Nintendo, 'Mobile':game.Mobile})

    except Game.DoesNotExist:
       game = None
       edit = False

    try:
       studio = GameStudio.objects.get(user=request.user)
       if game.studio.name == studio.name:
           edit = True

    except GameStudio.DoesNotExist:
       studio = None
       game = None
       edit = False

    if request.method == 'POST':
        form = GameRegisterForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save(commit=True)

            return show_profile(request)

    return render(request, 'panda/edit_game_profile.html', {'game': game, 'edit':edit, 'form': form, 'studio':studio})




#Helper Functions

def check_comment(comment_id):
    try:
        comment = Comment.objects.get(id = comment_id)

    except Comment.DoesNotExist:
        comment = None

    return comment

def check_player_user(user):
    try:
        player = Player.objects.get(user=user)

    except Player.DoesNotExist:
       player = None

    return player

def check_studio_user(user):
    try:
       studio = GameStudio.objects.get(user = user)

    except GameStudio.DoesNotExist:
       studio = None

    return studio


def check_player(player_name_slug): #Check if trying to acces valid user page
    try:
        player = Player.objects.get(slug = player_name_slug)

    except Player.DoesNotExist:
        player = None

    return player

def check_game(game_name_slug): #Check if trying to valid access game page
    try:
        game = Game.objects.get(slug = game_name_slug)

    except Game.DoesNotExist:
        game = None

    return game

def user_check(request, game_name_slug):  #Get details abouit current user
    studio_warning = False #Indicator if studio attempting to rate

    try:
        game = Game.objects.get(slug= game_name_slug)

    except Game.DoesNotExist:
       game = None

    try:
         player = Player.objects.get(user = request.user)

    except Player.DoesNotExist:
       studio_warning = True
       game = None
       player = None

    return studio_warning,game,player




#Google search requirements

def sitemap(request):

    context_dict = { }

    return render(request, 'panda/sitemap.xml', context=context_dict)

def google_veri(request):

    context_dict = { }

    return render(request, 'panda/googleb00694232a77d6d0.html', context=context_dict)


