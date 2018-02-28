from django import forms
from django.contrib.auth.models import User
from panda.models import Player



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')

class PlayerProfileForm(forms.ModelForm):

    class Meta:
        model = Player

        fields = ('Bio','Steam', 'PSN', 'Xbox','Nintendo', 'picture')

