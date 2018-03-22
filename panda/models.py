from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from datetime import datetime

STATUS = (
    ('Draft', 'Draft'),
    ('Published', 'Published'),
    ('Disabled', 'Disabled'),
)

USER_ROLES = (
    ('Admin', 'Admin'),
    ('Publisher', 'Publisher'),
)



User = settings.AUTH_USER_MODEL

class GameStudio(models.Model):  #Game Studios that make multiplayer games
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique = True)
    bio = models.CharField(max_length=500, null = True, blank= True)
    TwitterHandle = models.CharField(max_length=15, null=True, blank=True)
    picture = models.ImageField(upload_to='studio_images', blank=True)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwaargs):
        self.slug = slugify(self.name)
        super(GameStudio, self).save(*args, **kwaargs)

    def __str__(self):
        return self.name


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Bio = models.CharField(max_length=500, null = True, blank= True)
    Steam = models.CharField(max_length=31, null = True, blank= True)
    PSN = models.CharField(max_length=16, null = True, blank= True)
    Xbox = models.CharField(max_length=15, null = True, blank= True)
    Nintendo = models.CharField(max_length=10, null = True, blank= True)
    rating =  models.FloatField(default = -1.0)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    user_votes = models.IntegerField(default='0')
    user_roles = models.CharField(choices=USER_ROLES, max_length=10)

    approved = models.BooleanField(default = False)

    slug = models.SlugField(unique = True)

    def save(self, *args, **kwaargs):
        self.slug = slugify(self.user.username)
        super(Player, self).save(*args, **kwaargs)

    def __str__(self):

        return self.user.username

    def make_game_rating(self,ratee, rating): #Enforce many to one relation by using external helper function
        try:
            r = GameRating.objects.get(player=self, rated=ratee)
            r.value = rating

        except GameRating.DoesNotExist:
            r = GameRating(player=self, rated=ratee, value = rating)

        r.save()
        ratee.average_rating()

    def make_player_rating(self,ratee, rating): #Enforce many to one relation by using external helper function
        try:
            r = PlayerRating.objects.get(player=self, rated_player=ratee)
            r.value = rating

        except PlayerRating.DoesNotExist:
            r = PlayerRating(player=self, rated_player=ratee, value = rating)

        r.save()
        ratee.average_rating()

    def average_rating(self):
        query = PlayerRating.objects.filter(rated_player=self)
        self.rating = average(query)
        self.save()
        return self.rating

class Comment(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE,)
    comment = models.CharField(max_length=200, null = True, blank= True)

    def __str__(self):
        toString = self.player.user.username +  ' : ' + self.comment
        return toString

class Game(models.Model):  #

    NONE = 'NON'
    ACTION = 'ACT'
    ADVENTURE = 'ADV'
    ROLEPLAYING = 'ROL'
    MMO = 'MMO'
    FPS = 'FPS'
    SPO ='SPO'

    CATERGORY = (
        (ACTION, 'Action'),
        (ADVENTURE, 'Adventure'),
        (ROLEPLAYING, 'Roleplaying'),
        (MMO, 'MMO'),
        (FPS, 'FPS'),
        (SPO, 'Sport'),
    )

    studio = models.ForeignKey(GameStudio, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null = False, unique =True)
    players = models.ManyToManyField(Player, blank= True, related_name='casual')
    comp_players = models.ManyToManyField(Player, blank=True, related_name='comp')
    extract = models.CharField(max_length=1000, blank= False, default = 'Extract missing')
    site = models.URLField(null = True)
    date = models.DateField(null = True)
    catergory = models.CharField(max_length=3, choices=CATERGORY, default = NONE)
    picture = models.ImageField(upload_to='game_images', blank=True)

    steam_id = models.IntegerField(default = None, null=True, blank= True)

    rating = models.FloatField(default = -1)
    comments = models.ManyToManyField(Comment, blank= True)

    Playstation = models.BooleanField(default = False)
    Xbox = models.BooleanField(default = False)
    PC = models.BooleanField(default = False)
    Nintendo = models.BooleanField(default = False)
    Mobile = models.BooleanField(default = False)

    slug = models.SlugField(unique = True)

    def save(self, *args, **kwaargs):
        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwaargs)

    def __str__(self):
        return self.name

    def average_rating(self):
        query = GameRating.objects.filter(rated=self)
        self.rating = average(query)
        self.save()
        return self.rating

class GameRating(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    rated = models.ForeignKey(Game, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        toString = self.player.user.username +  ' : ' + str(self.value)
        return toString

class PlayerRating(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player')
    rated_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='rated_player')
    value = models.IntegerField()

    def __str__(self):
        toString = self.rating_user.user.username +  ' : ' + str(self.value)
        return toString

def average(query):
    count = 0
    sum = 0
    average = -1.0
    if query.exists():
        for rating in query:
            sum += rating.value
            count += 1
        average = sum/count
        average = round(average, 2)
    return average


class ForumCategory(models.Model):
    created_by = models.ForeignKey(User)
    title = models.CharField(max_length=1000)
    is_votable = models.BooleanField(default=False)
    color = models.CharField(max_length=20, default="#999999")
    created_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=1000)
    is_active = models.BooleanField(default=False)
    description = models.TextField()
    parent = models.ForeignKey('self', blank=True, null=True)

    def get_topics(self):
        topics = Topic.objects.filter(category=self, status='Published')
        return topics

    def __str__(self):
        return self.title

class Vote(models.Model):
    TYPES = (
        ("U", "Up"),
        ("D", "Down"),
    )
    user = models.ForeignKey(User)
    type = models.CharField(choices=TYPES, max_length=1)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

class Topic(models.Model):
    title = models.CharField(max_length=2000)
    description = models.TextField()
    created_by = models.ForeignKey(User)
    status = models.CharField(choices=STATUS, max_length=10)
    category = models.ForeignKey(ForumCategory)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    no_of_views = models.IntegerField(default='0')
    slug = models.SlugField(max_length=1000)
    no_of_likes = models.IntegerField(default='0')
    votes = models.ManyToManyField(Vote)

    def get_comments(self):
        comments = Comment.objects.filter(topic=self, parent=None)
        return comments

    def get_all_comments(self):
        comments = Comment.objects.filter(topic=self)
        return comments


    def up_votes_count(self):
        return self.votes.filter(type="U").count()

    def down_votes_count(self):
        return self.votes.filter(type="D").count()  

    def __str__(self):
        return self.title

class ForumComment(models.Model):
    comment = models.TextField(null=True, blank=True)
    commented_by = models.ForeignKey(User, related_name="commented_by")
    topic = models.ForeignKey(Topic, related_name="topic_comments")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="comment_parent")

    votes = models.ManyToManyField(Vote)

    def get_comments(self):
        comments = self.comment_parent.all()
        return comments

    def up_votes_count(self):
        return self.votes.filter(type="U").count()

    def down_votes_count(self):
        return self.votes.filter(type="D").count()

class ReportingMessage(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)

class ApprovalRequest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)