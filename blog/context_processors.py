from django.db.models import Count, Q
from .models import Category, Post
from taggit.models import Tag


def blog_context(request):
    # دسته‌بندی‌ها
    categories = Category.objects.annotate(
        post_count=Count("post", filter=Q(post__status="published"))
    ).filter(post_count__gt=0)

    # برچسب‌های محبوب
    popular_tags = (
        Tag.objects.annotate(post_count=Count("taggit_taggeditem_items"))
        .filter(post_count__gt=0)
        .order_by("-post_count")[:10]
    )

    # آمار کلی
    total_posts = Post.objects.filter(status="published").count()
    total_categories = Category.objects.count()

    return {
        "sidebar_categories": categories,
        "sidebar_popular_tags": popular_tags,
        "total_posts": total_posts,
        "total_categories": total_categories,
    }
