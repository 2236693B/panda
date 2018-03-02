from django import forms
from django.contrib.auth.models import User
from panda.models import Player, GameRating, Comment, Game, GameStudio
import datetime



class GameRatingForm (forms.ModelForm):
    INTEGER_CHOICES= [tuple([x,x]) for x in range(1,32)]

    value = forms.ChoiceField(required= True, choices=[(x, x) for x in range(1, 6)])

    class Meta:
        model = GameRating
        fields = ('value',)

class GameCommentForm (forms.ModelForm):
    value = forms.CharField(required = True, widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))

    class Meta:
        model = Comment
        fields = ('value',)

class PlayerRatingForm (forms.ModelForm):
    INTEGER_CHOICES= [tuple([x,x]) for x in range(1,32)]

    value = forms.ChoiceField(required= True, choices=[(x, x) for x in range(1, 6)])

    class Meta:
        model = GameRating
        fields = ('value',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')

class StudioProfileForm(forms.ModelForm):


    class Meta:
        model = GameStudio
        fields = ('name',)
        exclude = ('user',)


class PlayerProfileForm(forms.ModelForm):

    Bio = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))

    class Meta:
        model = Player
        fields = ('Bio','Steam', 'PSN', 'Xbox','Nintendo', 'picture')

class GameRegisterForm (forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(format="%d/%m/%Y"))

    class Meta:
        model = Game
        fields = ('name', 'extract', 'site','date','catergory','picture', 'Playstation', 'Xbox', 'PC', 'Nintendo', 'Mobile')

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date