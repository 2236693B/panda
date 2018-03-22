from django import template
from panda.models import ForumCategory, Player
from django.db.models import Count
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

register = template.Library()


@register.assignment_tag()
def get_categories():
    all_categories = ForumCategory.objects.filter(is_active=True).annotate(num_topics=Count('topic')).order_by('-num_topics')[:10]
    return all_categories

@register.filter
def is_topic_like(topic_id, user_id):
    user_topic = UserTopics.objects.filter(topic_id=topic_id, user_id=user_id).first()
    if user_topic:
        if user_topic.is_like:
            return True
    return False

@register.filter
def sub_comments(sub_comment):
    l = []
    reply = sub_comment.comment_parent.all()
    if reply:
        l.append(sub_comment)
        for sc in reply:
            l.extend(sub_comments(sc))
        return l
    return [sub_comment]
