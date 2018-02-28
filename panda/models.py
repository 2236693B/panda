from django.db import models
from django.contrib.auth.models import User

class GameStudio(models.Model):  #Game Studios that make multiplayer games
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

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

class Game(models.Model):  #

    NONE = 'NON'
    ACTION = 'ACT'
    ADVENTURE = 'ADV'
    ROLEPLAYING = 'ROL'
    MMO = 'MMO'
    FPS = 'FPS'
    SPO ='SPO'

    CATEGORIES = (
        (NONE, 'None'),
        (ACTION, 'Action'),
        (ADVENTURE, 'Adventure'),
        (ROLEPLAYING, 'Roleplaying'),
        (MMO, 'MMO'),
        (FPS, 'FPS'),
        (SPO, 'SPO'),
    )

    studio = models.ForeignKey(GameStudio, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null = False)
    players = models.ManyToManyField(Player, blank= True)
    extract = models.CharField(max_length=500, blank= False, default = 'Extract missing')
    site = models.URLField(null = True)
    date = models.DateField(null = True)
    catergory = models.CharField(max_length=3, choices=CATEGORIES, default = NONE)

    rating = models.FloatField(default = -1.0)

    Playstation = models.BooleanField(default = False)
    Xbox = models.BooleanField(default = False)
    PC = models.BooleanField(default = False)
    Nintendo = models.BooleanField(default = False)
    Mobile = models.BooleanField(default = False)


    def __str__(self):
        return self.name

    def average_rating(self):
        query = GameRating.objects.filter(rated=self)
        self.rating = average(query)
        self.save()
        return self.rating

class GameRating(models.Model):

    #class Meta:
        #unique_together = (('user', 'rated'),)

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    rated = models.ForeignKey(Game, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        toString = self.player.user.username +  ' : ' + str(self.value)
        return toString

class PlayerRating(models.Model):

    #class Meta:
        #unique_together = (('user', 'rated'),)

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


