from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import hashlib
from datetime import datetime

STATUS = (
    ('Draft', 'Draft'),
    ('Published', 'Published'),
    ('Disabled', 'Disabled'),
)

USER_ROLES = (
    ('Admin', 'Admin'),
    ('Publisher', 'Publisher'),
)

User = settings.AUTH_USER_MODEL

class GameStudio(models.Model):  #Game Studios that make multiplayer games
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique = True)

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

    slug = models.SlugField(unique = True)

    #new properties
    user_votes = models.IntegerField(default ='0')
    user_roles = models.CharField(choices=USER_ROLES, max_length=10)

    def save(self, *args, **kwaargs):
        self.slug = slugify(self.user.username)
        super(Player, self).save(*args, **kwaargs)

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


    #new functions for forum
    def get_no_of_up_votes(self):
        user_topics = UserTopics.objects.filter(user=self.user)
        votes = 0
        for topic in user_topics:
            votes += topic.no_of_votes
        return votes

    def get_no_of_down_votes(self):
        user_topics = UserTopics.objects.filter(user=self.user)
        votes = 0
        for topic in user_topics:
            votes += topic.no_of_down_votes
        return votes

    def get_topics(self):
        topics = Topic.objects.filter(created_by=self.user)
        return topics

    def get_followed_topics(self):
        topics = UserTopics.objects.filter(user=self.user, is_followed=True)
        topics = Topic.objects.filter(id__in=topics.values_list('topic', flat=True))
        return topics

    def get_liked_topics(self):
        topics = UserTopics.objects.filter(user=self.user, is_like=True)
        topics = Topic.objects.filter(id__in=topics.values_list('topic', flat=True))
        return topics

    def get_timeline(self):
        timeline = Timeline.objects.filter(user=self.user).order_by('-created_on')
        return timeline

    def get_user_topic_tags(self):
        tags = Tags.objects.filter(id__in=self.get_topics().values_list('tags', flat=True))
        return tags

    def get_user_topic_categories(self):
        categories = ForumCategory.objects.filter(id__in=self.get_topics().values_list('category', flat=True))
        return categories
        # return []

    def get_user_suggested_topics(self):
        categories = ForumCategory.objects.filter(id__in=self.get_topics().values_list('category', flat=True))
        topics = Topic.objects.filter(category__id__in=categories.values_list('id', flat=True))
        return topics
        # return []

class Forum_Comment(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE,)
    comment = models.CharField(max_length=200, null = True, blank= True)
    #properites for forum
    commented_by = models.ForeignKey(User, related_name="commented_by")
    topic = models.ForeignKey(Topic, related_name="topic_comments")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="comment_parent")
    mentioned = models.ManyToManyField(User, related_name="mentioned_users")
    votes = models.ManyToManyField(Vote)

    def get_comments(self):
        comments = self.comment_parent.all()
        return comments

    def up_votes_count(self):
        return self.votes.filter(type="U").count()

    def down_votes_count(self):
        return self.votes.filter(type="D").count()

    def __str__(self):
        toString = self.player.user.username +  ' : ' + self.comment
        return toString




class Comment(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE,)
    comment = models.CharField(max_length=200, null = True, blank= True)

    def __str__(self):
        toString = self.player.user.username +  ' : ' + self.comment
        return toString

class Game(models.Model):  #

    NONE = 'NON'
    ACTION = 'ACT'
    ADVENTURE = 'ADV'
    ROLEPLAYING = 'ROL'
    MMO = 'MMO'
    FPS = 'FPS'
    SPO ='SPO'

    CATERGORY = (
        (ACTION, 'Action'),
        (ADVENTURE, 'Adventure'),
        (ROLEPLAYING, 'Roleplaying'),
        (MMO, 'MMO'),
        (FPS, 'FPS'),
        (SPO, 'Sport'),
    )

    studio = models.ForeignKey(GameStudio, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null = False, unique =True)
    players = models.ManyToManyField(Player, blank= True)
    extract = models.CharField(max_length=500, blank= False, default = 'Extract missing')
    site = models.URLField(null = True)
    date = models.DateField(null = True)
    catergory = models.CharField(max_length=3, choices=CATERGORY, default = NONE)
    picture = models.ImageField(upload_to='game_images', blank=True)

    steam_id = models.IntegerField(default = None, null=True, blank= True)

    rating = models.FloatField(blank = True)
    comments = models.ManyToManyField(Comment, blank= True)

    Playstation = models.BooleanField(default = False)
    Xbox = models.BooleanField(default = False)
    PC = models.BooleanField(default = False)
    Nintendo = models.BooleanField(default = False)
    Mobile = models.BooleanField(default = False)

    slug = models.SlugField(unique = True)


    def save(self, *args, **kwaargs):
        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwaargs)

    def __str__(self):
        return self.name

    def average_rating(self):
        query = GameRating.objects.filter(rated=self)
        self.rating = average(query)
        self.save()
        return self.rating

class GameRating(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    rated = models.ForeignKey(Game, on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        toString = self.player.user.username +  ' : ' + str(self.value)
        return toString

class PlayerRating(models.Model):

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


# tags created for topic
class Tags(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)

    def get_topics(self):
        topics = Topic.objects.filter(tags__in=[self], status='Published')
        return topics

class ForumCategory(models.Model):
    created_by = models.ForeignKey(User)
    title = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=False)
    color = models.CharField(max_length=20, default="#999999")
    is_votable = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=1000)
    description = models.TextField()
    parent = models.ForeignKey('self', blank=True, null=True)

    def get_topics(self):
        topics = Topic.objects.filter(category=self, status='Published')
        return topics

    def __str__(self):
        return self.title

class Vote(models.Model):
    TYPES = (
        ("U", "Up"),
        ("D", "Down"),
    )
    user = models.ForeignKey(User)
    type = models.CharField(choices=TYPES, max_length=1)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class Topic(models.Model):
    title = models.CharField(max_length=2000)
    description = models.TextField()
    created_by = models.ForeignKey(User)
    status = models.CharField(choices=STATUS, max_length=10)
    category = models.ForeignKey(ForumCategory)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now=True)
    no_of_views = models.IntegerField(default='0')
    slug = models.SlugField(max_length=1000)
    tags = models.ManyToManyField(Tags)
    no_of_likes = models.IntegerField(default='0')
    votes = models.ManyToManyField(Vote)

    def get_comments(self):
        comments = Comment.objects.filter(topic=self, parent=None)
        return comments

    def get_all_comments(self):
        comments = Comment.objects.filter(topic=self)
        return comments

    def get_last_comment(self):
        comments = Comment.objects.filter(topic=self).order_by('-updated_on').first()
        return comments

    def get_topic_users(self):
        comment_user_ids = Comment.objects.filter(topic=self).values_list('commented_by', flat=True)
        liked_users_ids = UserTopics.objects.filter(topic=self, is_like=True).values_list('user', flat=True)
        followed_users = UserTopics.objects.filter(topic=self, is_followed=True).values_list('user', flat=True)
        all_users = list(comment_user_ids) + list(liked_users_ids) + list(followed_users) + [self.created_by.id]
        users = UserProfile.objects.filter(user_id__in=set(all_users))
        return users

    def up_votes_count(self):
        return self.votes.filter(type="U").count()

    def down_votes_count(self):
        return self.votes.filter(type="D").count()

    def __str__(self):
        return self.title


class UserTopics(models.Model):
    user = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)
    is_followed = models.BooleanField(default=False)
    followed_on = models.DateField(null=True, blank=True)
    no_of_votes = models.IntegerField(default='0')
    no_of_down_votes = models.IntegerField(default='0')
    is_like = models.BooleanField(default=False)


# user activity
class Timeline(models.Model):
    content_type = models.ForeignKey(ContentType, related_name="content_type_timelines")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    namespace = models.CharField(max_length=250, default="default", db_index=True)
    event_type = models.CharField(max_length=250, db_index=True)
    user = models.ForeignKey(User, null=True)
    data = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        index_together = [("content_type", "object_id", "namespace"), ]
        ordering = ['-created_on']


class Attachment(models.Model):
    file_prepend = "forum_topic/attachments/"
    uploaded_by = models.ForeignKey(User, related_name='attachments_user')
    created_on = models.DateTimeField(auto_now_add=True)
    attached_file = models.FileField(
        max_length=500, null=True, blank=True, upload_to=img_url)
    comment = models.ForeignKey(Comment)
