from django.db import models
from django.contrib.auth.models import User

class GameStudio(models.Model):  #Game Studios that make multiplayer games
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Player(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Bio = models.CharField(max_length=200, null = True, blank= True)
    Steam = models.CharField(max_length=200, null = True, blank= True)
    PSN = models.CharField(max_length=200, null = True, blank= True)
    Xbox = models.CharField(max_length=200, null = True, blank= True)
    average = 0
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):

        return self.user.username

    def make_game_rating(self,ratee, rating): #Enforce many to one relation by using external helper function
        try:
            r = GameRating.objects.get(user=self, rated=ratee)
            r.value = rating

        except GameRating.DoesNotExist:
            r = GameRating(user=self, rated=ratee, value = rating)

        r.save()

class Game(models.Model):  #
    studio = models.ForeignKey(GameStudio, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null = True, blank= True)
    players = models.ManyToManyField(Player, blank= True)

    def __str__(self):
        return self.name

    def average_rating(self):
        query = GameRating.objects.filter(rated=self)
        count = 0
        sum = 0
        if query.exists():
            for rating in query:
                sum += rating.value
                count += 1
                return sum/count
        else:
            return "N/a"

class GameRating(models.Model):

    #class Meta:
        #unique_together = (('user', 'rated'),)

    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    rated = models.ForeignKey(Game, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        toString = self.user.user.username +  ' : ' + str(self.value)
        return toString

