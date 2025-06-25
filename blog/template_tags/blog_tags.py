from django import template
from django.db.models import Count, Q
from ..models import Category, Post
from taggit.models import Tag

register = template.Library()


@register.inclusion_tag("blog/tags/categories.html")
def get_categories():
    categories = Category.objects.annotate(
        post_count=Count("post", filter=Q(post__status="published"))
    ).filter(post_count__gt=0)
    return {"categories": categories}


@register.inclusion_tag("blog/tags/popular_tags.html")
def get_popular_tags(count=10):
    tags = (
        Tag.objects.annotate(post_count=Count("taggit_taggeditem_items"))
        .filter(post_count__gt=0)
        .order_by("-post_count")[:count]
    )
    return {"tags": tags}


@register.inclusion_tag("blog/tags/recent_posts.html")
def get_recent_posts(count=5):
    posts = Post.objects.filter(status="published").order_by("-published_at")[:count]
    return {"posts": posts}


@register.simple_tag
def get_post_count():
    return Post.objects.filter(status="published").count()


@register.simple_tag
def get_category_count():
    return Category.objects.count()
