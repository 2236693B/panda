from django import forms
from django.contrib.auth.models import User
from panda.models import Player, GameRating, Comment, Game, GameStudio, ReportingMessage, ApprovalRequest, ForumCategory, Topic,ForumComment
import datetime
from django.template.defaultfilters import slugify

INTEGER_CHOICES= [tuple([x,x]) for x in range(0,6)] #Limit rating choices from 0-5




from django import forms
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.template import loader


class ContactForm(forms.Form):
    """
    The base contact form class from which all contact form classes
    should inherit.
    """
    name = forms.CharField(max_length=100,
                           label=_(u'Your name'))
    email = forms.EmailField(max_length=200,
                             label=_(u'Your email address'))
    body = forms.CharField(widget=forms.Textarea,
                           label=_(u'Your message'))

    from_email = settings.DEFAULT_FROM_EMAIL

    recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]

    subject_template_name = "contact_form/contact_form_subject.txt"

    template_name = 'contact_form/contact_form.txt'

    def __init__(self, data=None, files=None, request=None,
                 recipient_list=None, *args, **kwargs):
        if request is None:
            raise TypeError("Keyword argument 'request' must be supplied")
        self.request = request
        if recipient_list is not None:
            self.recipient_list = recipient_list
        super(ContactForm, self).__init__(data=data, files=files,
                                          *args, **kwargs)

    def message(self):
        """
        Render the body of the message to a string.
        """
        template_name = self.template_name() if \
            callable(self.template_name) \
            else self.template_name
        return loader.render_to_string(
            template_name, self.get_context(), request=self.request
        )

    def subject(self):
        """
        Render the subject of the message to a string.
        """
        template_name = self.subject_template_name() if \
            callable(self.subject_template_name) \
            else self.subject_template_name
        subject = loader.render_to_string(
            template_name, self.get_context(), request=self.request
        )
        return ''.join(subject.splitlines())

    def get_context(self):
        """
        Return the context used to render the templates for the email
        subject and body.
        By default, this context includes:
        * All of the validated values in the form, as variables of the
          same names as their fields.
        * The current ``Site`` object, as the variable ``site``.
        * Any additional variables added by context processors (this
          will be a ``RequestContext``).
        """
        if not self.is_valid():
            raise ValueError(
                "Cannot generate Context from invalid contact form"
            )
        return dict(self.cleaned_data, site=get_current_site(self.request))

    def get_message_dict(self):
        """
        Generate the various parts of the message and return them in a
        dictionary, suitable for passing directly as keyword arguments
        to ``django.core.mail.send_mail()``.
        By default, the following values are returned:
        * ``from_email``
        * ``message``
        * ``recipient_list``
        * ``subject``
        """
        if not self.is_valid():
            raise ValueError(
                "Message cannot be sent from invalid contact form"
            )
        message_dict = {}
        for message_part in ('from_email', 'message',
                             'recipient_list', 'subject'):
            attr = getattr(self, message_part)
            message_dict[message_part] = attr() if callable(attr) else attr
        return message_dict

    def save(self, fail_silently=False):
        """
        Build and send the email message.
        """
        send_mail(fail_silently=fail_silently, **self.get_message_dict())


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
    today = datetime.date.today()
    YEARS = [x for x in range(1970, today.year+1)]  # Limit rating choices from 0-5
    date =forms.DateField(initial=datetime.date.today, widget=forms.SelectDateWidget(years=YEARS))

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

class ApprovingPlayerForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))

    class Meta:
        model = ApprovalRequest
        fields = ('message',)

