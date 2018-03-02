from django import forms
from django.contrib.auth.models import User
from panda.models import Player, GameRating, Comment, Game
import datetime



class GameRatingForm (forms.ModelForm):
    INTEGER_CHOICES= [tuple([x,x]) for x in range(1,32)]

    value = forms.ChoiceField(choices=[(x, x) for x in range(1, 6)])

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

class GameRegisterForm (forms.ModelForm,):
    date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(format="%d/%m/%Y"))

    class Meta:
        model = Game
        fields = ('name', 'extract', 'site','date','catergory','picture', 'Playstation', 'Xbox', 'PC', 'Nintendo', 'Mobile')

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date