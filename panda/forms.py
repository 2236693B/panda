from django import forms
from django.contrib.auth.models import User
from panda.models import Player, GameRating, Comment, Game, GameStudio
import datetime

INTEGER_CHOICES= [tuple([x,x]) for x in range(0,6)] #Limit rating choices from 0-5

#Form for Player to rate game
class GameRatingForm (forms.ModelForm):

    value = forms.ChoiceField(required= True, choices=INTEGER_CHOICES)

    class Meta:
        model = GameRating
        fields = ('value',)

#Form for Player to comment on game
class GameCommentForm (forms.ModelForm):
    value = forms.CharField(required = True, widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))

    class Meta:
        model = Comment
        fields = ('value',)

#Form for Player to rate another player
class PlayerRatingForm (forms.ModelForm):

    value = forms.ChoiceField(required= True, choices=INTEGER_CHOICES)

    class Meta:
        model = GameRating
        fields = ('value',)

#Form for base user, used by both Player and Studio
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')

#Details form for Studio, user for registeration and changing details
class StudioProfileForm(forms.ModelForm):

    class Meta:
        model = GameStudio
        fields = ('name',)
        exclude = ('user',)

#Details form for Player, user for registeration and changing details
class PlayerProfileForm(forms.ModelForm):
    Bio = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))

    class Meta:
        model = Player
        fields = ('Bio','Steam', 'PSN', 'Xbox','Nintendo', 'picture')

#Details form for Game, user for registeration and changing details by studio
class GameRegisterForm (forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(format="%d/%m/%Y"))

    class Meta:
        model = Game
        fields = ('name', 'extract', 'site','date','catergory','picture', 'Playstation', 'Xbox', 'PC', 'Nintendo', 'Mobile')

    def clean_date(self):
        date = self.cleaned_data['date']

        # Check to make sure date is valid i.e not in the future
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date