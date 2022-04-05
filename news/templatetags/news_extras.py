

from django import template
from news.models import Category, Post
from django.conf import settings
from django.db.models import Count
from django.contrib.auth import get_user_model


User = get_user_model()
register = template.Library()


@register.inclusion_tag('news/list_category.html')
def get_list_category():
    number_posts_category = Category.objects.annotate(number=Count('post'))
    return {'number_posts_category': number_posts_category}


@register.inclusion_tag('news/list_author.html')
def get_list_author():
    number_author_category = User.objects.annotate(
        number=Count('post')).filter(is_author=True, number__gt=0)
    return {'number_author_category': number_author_category}


@register.inclusion_tag('news/author_full_list_teg.html')
def author_full_list():
    authors = User.objects.annotate(number=Count('post')).filter(
        is_author=True, number__gt=0).select_related('profileauthor__category')
    return {'authors': authors}
