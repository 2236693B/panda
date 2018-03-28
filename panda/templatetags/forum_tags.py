from django import template
from panda.models import ForumCategory
from django.db.models import Count

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()

except ImportError:
    from django.contrib.auth.models import User
    from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('forum/left_menu.html')
def get_categories():
    categories = ForumCategory.objects.annotate(num_topics=Count('topic')).order_by('-num_topics')[:10]
    return {'test': True, 'categories': categories}

