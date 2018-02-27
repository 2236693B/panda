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

class Game(models.Model):  #
    studio = models.ForeignKey(GameStudio, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null = True, blank= True)
    average = 0
    players = models.ManyToManyField(Player, blank= True)

    def __str__(self):
        return self.name

    def average_rating(self):
        query = GameRating.objects.filter(rated=self)
        count = 0
        sum = 0

        for rating in query:
            sum += rating.value
            count += 1
        if query.exists():
            self.average = sum/count
            return self.average
        else:
            return "N/a"

class GameRating(models.Model):

    #class Meta:
        #unique_together = (('user', 'rated'),)

    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    rated = models.ForeignKey(Game, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        toString = self.user.name +  ' : ' + str(self.value)
        return toString

def make_rating(ratee, rater, rating):   #Enforce many to one relation by using external helper function

    try:
        r = GameRating.objects.get(user=rater, rated=ratee)
        r.value = rating
        ratee.average_rating()

    except GameRating.DoesNotExist:
        r = GameRating(user=rater, rated=ratee, value = rating)
        ratee.average_rating()

    r.save()

