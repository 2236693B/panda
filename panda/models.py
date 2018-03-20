from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class GameStudio(models.Model):  #Game Studios that make multiplayer games
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique = True)

    def __str__(self):
        return self.name


class Player(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Bio = models.CharField(max_length=200, null = True, blank= True)
    Steam = models.CharField(max_length=31, null = True, blank= True)
    PSN = models.CharField(max_length=16, null = True, blank= True)
    Xbox = models.CharField(max_length=15, null = True, blank= True)
    Nintendo = models.CharField(max_length=10, null = True, blank= True)
    rating =  models.FloatField(default = -1.0)
    picture = models.ImageField(upload_to='profile_images', blank=True)

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
        self.rating = round(average(query), 2)
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
    extract = models.CharField(max_length=500, blank= False, default = 'Extract missing')
    site = models.URLField(null = True)
    date = models.DateField(null = True)
    catergory = models.CharField(max_length=3, choices=CATERGORY, default = NONE)
    picture = models.ImageField(upload_to='game_images', blank=True)

    steam_id = models.IntegerField(default = None, null=True, blank= True)

    rating = models.FloatField(default = -1.0)
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
        self.rating = round(average(query),2)
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
    return average

class ReportingMessage(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)


