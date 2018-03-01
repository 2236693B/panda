from django import forms
from django.contrib.auth.models import User
from panda.models import Player, GameRating, Comment


class GameRatingForm (forms.ModelForm):
    value = forms.IntegerField(required = True, max_value = 5, min_value = 0)

    class Meta:
        model = GameRating
        fields = ('value',)

class GameCommentForm (forms.ModelForm):
    value = forms.CharField(required = True)

    class Meta:
        model = Comment
        fields = ('value',)

class PlayerRatingForm (forms.ModelForm):
    value = forms.IntegerField(required = True, max_value = 5, min_value = 0)

    class Meta:
        model = GameRating
        fields = ('value',)



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')

class PlayerProfileForm(forms.ModelForm):

    class Meta:
        model = Player

        fields = ('Bio','Steam', 'PSN', 'Xbox','Nintendo', 'picture')

