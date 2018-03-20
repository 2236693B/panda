from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect#, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from panda.forms import UserForm, PlayerProfileForm, GameRatingForm, GameCommentForm , PlayerRatingForm, GameRegisterForm, StudioProfileForm, CategoryForm, TopicForm, ForumCommentForm
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DetailView, DeleteView, View
from django.views.generic.edit import FormView
from django.db.models import Q


from .models import Game, Player,GameRating, Comment, PlayerRating, GameStudio, ForumCategory, STATUS, Topic, ForumComment

import requests as r
import json

def sitemap(request):

    context_dict = { }

    return render(request, 'panda/sitemap.xml', context=context_dict)

def google_veri(request):

    context_dict = { }

    return render(request, 'panda/googleb00694232a77d6d0.html', context=context_dict)

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

def contact_us(request):

    context_dict = {}
    return render(request, 'panda/contact_us.html', context = context_dict)

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

#Show studio or player's own profile
@login_required
def show_profile(request):

    context_dict = {}

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

        else:
            print(form.errors)

    return render(request, 'panda/edit_game_profile.html', {'game': game, 'edit':edit, 'form': form, 'studio':studio})



class DashboardView(TemplateView):
    template_name = 'forum_dashboard/forum_dashboard.html'







class CategoryList(ListView):
    model = ForumCategory
    template_name = 'forum_dashboard/categories.html'
    context_object_name = 'categories_list'

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        categories_list = ForumCategory.objects.filter(parent=None)
        context['categories_list'] = categories_list
        return context

    def post(self, request, *args, **kwargs):
        categories_list = self.model.objects.all()

        if request.POST.get('is_active') == 'True':
            forum_categories = forum_categories.filter(is_active=True)
        if request.POST.get('search_text', ''):
            forum_categories = forum_categories.filter(
                title_icontains=request.POST.get('search_text')
            )
        return render(request, self.template_name, {'categories_list':categories_list})


class CategoryDetailView(DetailView):
    model = ForumCategory
    template_name = 'forum_dashboard/view_category.html'
    slug_field = "slug"
    context_object_name ='forum_category'

    def get_object(self):
        return get_object_or_404(ForumCategory, slug=self.kwargs['slug'])


class CategoryAdd(CreateView):
    model = ForumCategory
    form_class = CategoryForm
    template_name = "forum_dashboard/category_add.html"
    

    def get_form_kwargs(self):
        kwargs = super(CategoryAdd, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        menu = form.save()
        if self.request.POST.get('parent'):
            menu.parent_id = self.request.POST.get('parent')
            menu.save()

        data = {'error': False, 'response': 'Successfully Created Category'}
        return JsonResponse(data)

    def form_invalid(self, form):
        data = {'error':True, 'response': form.errors}
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super(CategoryAdd, self).get_context_data(**kwargs)
        form = CategoryForm(self.request.GET)
        menus = ForumCategory.objects.filter(parent=None)
        context['form'] = form
        context['menus'] = menus
        return context

class CategoryDelete(DeleteView):
    model = ForumCategory
    slug_field = 'slug'
    template_name = "forum_dashboard/categories.html"

    def get_object(self):
        return get_object_or_404(ForumCategory, slug=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return JsonResponse({'error': False, 'response': 'Successfully Deleted Category'})        


class CategoryEdit(UpdateView):
    model = ForumCategory
    form_class = CategoryForm
    template_name = "forum_dashboard/category_add.html"
    context_object_name = 'category'

    def get_object(self):
        return get_object_or_404(ForumCategory, slug=self.kwargs['slug'])

    def get_form_kwargs(self):
        kwargs = super(CategoryEdit, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        menu = form.save()
        if self.request.POST.get('parent'):
            menu.parent_id = self.request.POST.get('parent')
            menu.save()
        data = {'error': False, 'response': 'Successfully Edited Category'}
        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse({'error': True, 'response': form.errors})

    def get_context_data(self, **kwargs):
        context = super(CategoryEdit, self).get_context_data(**kwargs)
        form = CategoryForm(self.request.GET)
        menus = ForumCategory.objects.filter(parent=None)
        context['form'] = form
        context['menus'] = menus
        return context

class DashboardTopicList(ListView):
    template_name = 'forum_dashboard/topics.html'
    context_object_name = "topic_list"

    def get_queryset(self):
        queryset = Topic.objects.all()
        search_text = self.request.POST.get('search_text')
        if search_text:
            queryset = queryset.filter(
                Q(title__icontains=search_text) | Q(created_by__username__icontains=search_text)
            )
        return queryset


class ForumIndexView(FormView):
    template_name = 'forum/topic_list.html'
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        topics = Topic.objects.filter(status='Publsihed')
        context['topic_list'] = topics
        return context

    def form_valid(self, form):
        user = User.objects.create(
            username=form.cleaned_data['username'], email=form.cleaned_data['email'])
        user.set_password(form.cleaned_data['password'])
        user.is_active = True
        user.save()
        UserProfile.objects.create(user=user, user_roles='Publisher')
        login(self.request, user)

        data = {'error': False, 'response': 'Successfully Created Badge'}
        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse({'error': True, 'response': form.errors})

class TopicAdd(CreateView):
    model = Topic
    form_class = TopicForm
    template_name = "forum/new_topic.html"

    def get_form_kwargs(self):
        kwargs = super(TopicAdd, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        topic = form.save()
        if self.request.POST['sub_category']:
            topic.category_id = self.request.POST['sub_category']
        topic.save()
        data = {'error': False, 'response': 'Successfully Created Topic'}
        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse({'error': True, 'response': form.errors})

    def get_context_data(self, **kwargs):
        context = super(TopicAdd, self).get_context_data(**kwargs)
        form = TopicForm(self.request.GET)
        context['form'] = form
        context['status'] = STATUS
        context['categories'] = ForumCategory.objects.filter(
            is_active=True, is_votable=True, parent=None)
        context['sub_categories'] = ForumCategory.objects.filter(
            is_active=True, is_votable=True).exclude(parent=None)
        return context
        
class TopicList(ListView):
    template_name = 'forum/topic_list.html'
    context_object_name = "topic_list"

    def get_queryset(self):
        if self.request.user.is_authenticated():
            query = Q(status='Published')|Q(created_by=self.request.user)

        else:
            query = Q(status='Published')
        queryset = Topic.objects.filter(query).order_by('created_on')
        return queryset
        
class TopicView(TemplateView):
    template_name = 'forum/view_topic.html'

    def get_object(self):
        return get_object_or_404(Topic, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(TopicView, self).get_context_data(**kwargs)
        context['topic'] = self.get_object()
        return context

class TopicDeleteView(DeleteView):
    model = Topic
    template_name = "forum/topic_delete.html"

    def get_object(self):
        if not hasattr(self, "object"):
            self.object = super(TopicDeleteView, self).get_object()
        return self.object

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({"error": False, "message": "deleted"})
        else:
            return super(TopicDeleteView, self).delete(request, *args, **kwargs)
            

class CommentVoteUpView(View):

    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get("pk"))
        vote = comment.votes.filter(user=request.user).first()
        if not vote:
            vote = Vote.objects.create(user=request.user, type="U")
            comment.votes.add(vote)
            comment.save()
            status = "up"
        elif vote and vote.type == "D":
            vote.delete()
            status = "removed"
        else:
            status = "neutral"
        return JsonResponse({"status": status})

class CommentVoteDownView(View):

    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get("pk"))
        vote = comment.votes.filter(user=request.user).first()
        if not vote:
            vote = Vote.objects.create(user=request.user, type="D")
            comment.votes.add(vote)
            comment.save()
            status = "down"
        elif vote and vote.type == "U":
            vote.delete()
            status = "removed"
        else:
            status = "neutral"
        return JsonResponse({"status": status})

class ForumCommentAdd(CreateView):
    model = Topic
    form_class = ForumCommentForm
    template_name = 'forum/view_topic.html'
    form_class = ForumCommentForm
    slug_field = 'slug'

    def get_form_kwargs(self):
        kwargs = super(ForumCommentAdd, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        comment = form.save()
        if self.request.POST['parent']:
            comment.parent_id = self.request.POST['parent']
            comment.save()

        data = {'error': False, 'response': 'Successfully Created Topic'}
        return JsonResponse(data)

    def form_invalid(self, form):
        return JsonResponse({'error': True, 'response': form.errors})

    def get_context_data(self, **kwargs):
        context = super(CommentAdd, self).get_context_data(**kwargs)
        form = CommentForm(self.request.GET)
        context['form'] = form
        return context

class ForumCommentDelete(DeleteView):
    model = ForumComment
    slug_field = 'comment_id'
    template_name = "forum_dashboard/categories.html"

    def get_object(self):
        return get_object_or_404(ForumComment, id=self.kwargs['comment_id'])

    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        if self.request.user == comment.commented_by:
            comment.delete()
            return JsonResponse({'error': False, 'response': 'Successfully Deleted Your Comment'})
        else:
            return JsonResponse({'error': False, 'response': 'Only commented user can delete this comment'})

class ForumCategoryList(ListView):
    queryset = ForumCategory.objects.filter(
        is_active=True, is_votable=True).order_by('created_on')
    template_name = 'forum/categories.html'
    context_object_name = "categories"
    paginate_by = '10'

class ForumCategoryView(ListView):
    template_name = 'forum/topic_list.html'

    def get_queryset(self, queryset=None):
        if self.request.user.is_authenticated():
            query = Q(status="Published")
        else:
            query = Q(status="Published")
        category = get_object_or_404(ForumCategory, slug=self.kwargs.get("slug"))
        topics = category.topic_set.filter(query)
        return topics

class TopicDetail(TemplateView):
    template_name = 'forum_dashboard/view_topic.html'

    def get_object(self):
        return get_object_or_404(Topic, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(TopicDetail, self).get_context_data(**kwargs)
        context['topic'] = self.get_object()
        return context

class TopicStatus(View):
    model = Topic
    slug_field = 'slug'

    def get_object(self):
        return get_object_or_404(Topic, slug=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        topic = self.get_object()
        if topic.status == 'Draft':
            topic.status = 'Published'
        elif topic.status == 'Published':
            topic.status = 'Draft'
        else:
            topic.status = 'Disabled'
        topic.save()
        return JsonResponse({'error': False, 'response': 'Successfully Updated Topic Status'}) 


class TopicVoteUpView(View):

    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, slug=kwargs.get("slug"))
        vote = topic.votes.filter(user=request.user).first()
        if not vote:
            vote = Vote.objects.create(user=request.user, type="U")
            topic.votes.add(vote)
            topic.save()
            status = "up"
        elif vote and vote.type == "D":
            vote.delete()
            status = "removed"
        else:
            status = "neutral"
        return JsonResonse({"status": status})

class TopicVoteDownView(View):

    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, slug=kwargs.get("slug"))
        vote = topic.votes.filter(user=request.user).first()
        if not vote:
            vote = Vote.objects.create(user=request.user, type="D")
            topic.votes.add(vote)
            topic.save()
            status = "down"
        elif vote and vote.type == "U":
            vote.delete()
            status="removed"
        else:
            status = "neutral"
        return JsonResponse({"status": status})

    

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







