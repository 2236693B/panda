from django import forms
from django.contrib.auth.models import User

from panda.models import Player, GameRating, Comment, Game, GameStudio, ForumCategory, Topic,ForumComment

from panda.models import Player, GameRating, Comment, Game, GameStudio, ReportingMessage

import datetime
from django.template.defaultfilters import slugify

INTEGER_CHOICES= [tuple([x,x]) for x in range(0,6)] #Limit rating choices from 0-5

#Form for Player to rate game
class GameRatingForm (forms.ModelForm):

    value = forms.ChoiceField(required= True, choices=INTEGER_CHOICES)

    class Meta:
        model = GameRating
        fields = ('value',)

#Form for Player to comment on game
class GameCommentForm (forms.ModelForm):
    comment = forms.CharField(required = True, widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))

    class Meta:
        model = Comment
        fields = ('comment',)

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

#Details form for Studio, used for registeration and changing details
class StudioProfileForm(forms.ModelForm):

    class Meta:
        model = GameStudio
        fields = ('name','bio', 'TwitterHandle', 'picture')
        exclude = ('user',)

#Details form for Player, used for registeration and changing details
class PlayerProfileForm(forms.ModelForm):
    Bio = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))

    class Meta:
        model = Player
        fields = ('Bio','Steam', 'PSN', 'Xbox','Nintendo', 'picture')

#Details form for Game, used for registeration and changing details by studio
class GameRegisterForm (forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(format="%d/%m/%Y"))

    class Meta:
        model = Game
        fields = ('name', 'extract', 'site','date','catergory','picture', 'Playstation', 'Xbox', 'PC', 'Nintendo', 'Mobile', 'steam_id')

    def clean_date(self):
        date = self.cleaned_data['date']

        # Check to make sure date is valid i.e not in the future
        if date > datetime.date.today():
            raise forms.ValidationError("The date cannot be in the future!")
        return date


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ForumCategory
        exclude = ('slug', 'created_by')

    def clean_title(self):
        if ForumCategory.objects.filter(slug=slugify(self.cleaned_data['title'])).exclude(id=self.instance.id):
            raise forms.ValidationError('Category with this Name already exists.')

        return self.cleaned_data['title']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CategoryForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CategoryForm, self).save(commit=False)
        instance.created_by = self.user
        instance.title = self.cleaned_data['title']
        if str(self.cleaned_data['is_votable']) == 'True':
            instance.is_votable = True
        else:
            instance.is_votable = False
        if str(self.cleaned_data['is_active']) == 'True':
            instance.is_active = True
        else:
            instance.is_active = False
        if not self.instance.id:
            instance.slug = slugify(self.cleaned_data['title'])

        if commit:
            instance.save()
        return instance
class TopicForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields["category"].widget.attrs = {"class": "form-control select2"}
        self.fields["title"].widget.attrs = {"class": "form-control"}
        self.fields["tags"].widget.attrs = {"class": "form-control tags"}

    tags = forms.CharField(required=False)

    class Meta:
        model = Topic
        fields = ("title", "category", "description", "tags")

    def clean_title(self):
         
        if Topic.objects.filter(slug=slugify(self.cleaned_data['title'])).exclude(id=self.instance.id):
            raise forms.ValidationError('Topic with this Name already exists.')

        return self.cleaned_data['title']

    def save(self, commit=True):
        instance = super(TopicForm, self).save(commit=False)
        instance.title = self.cleaned_data['title']
        instance.description = self.cleaned_data['description']
        instance.category = self.cleaned_data['category']
        if not self.instance.id:
            instance.slug = slugify(self.cleaned_data['title'])
            instance.created_by = self.user
            instance.status = 'Draft'
        if commit:
            instance.save()
        return instance

class ForumCommentForm(forms.ModelForm):

    class Meta:
        model = ForumComment
        fields = ('comment', 'topic')

    def clean_comment(self):
        if self.cleaned_data['comment']:
            return self.cleaned_data['comment']
        raise forms.ValidationError('This field is required')
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CommentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CommentForm, self).save(commit=False)
        instance.comment = self.cleaned_data['comment']
        instance.topic = self.cleaned_data['topic']
        if not self.instance.id:
            instance.commented_by = self.user
            if 'parent' in self.cleaned_data.keys() and self.cleaned_data['parent']:
                instance.parent = self.cleaned_data['parent']
        if commit:
            instance.save()
        return instance

class ReportingPlayerForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))

    class Meta:
        model = ReportingMessage
        fields = ('message',)

