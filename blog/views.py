from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import Post, Category
from .forms import CommentForm


def home(request):
    latest_posts = Post.objects.filter(status="published").order_by("-published_at")[:6]

    popular_post = Post.objects.filter(status="published").order_by("-views")[:3]

    context = {"latest_posts": latest_posts, "popular_posts": popular_post}

    return render(request, "blog/home.html", context)


def post_list(request):
    posts = Post.objects.filter(status="published").order_by("-published_at")

    paginator = Paginator(posts, 6)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "posts": page_obj}

    return render(request, "blog/post_list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")

    post.views += 1
    post.save()

    comments = post.comments.filter(is_approved=True, parent=None)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(
                request, "کامنت شما با موفقیت ثبت شد و پس از تایید نمایش داده خواهد شد."
            )
        return redirect("blog:post_detail", slug=slug)
    else:
        comment_form = CommentForm()

    related_post = Post.objects.filter(
        category=post.category, status="published"
    ).exclude(id=post.id)[:3]

    context = {
        "post": post,
        "comments": comments,
        "comment_form": comment_form,
        "related_post": related_post,
    }
    return render(request, "blog/post_detail.html", context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status="published").order_by(
        "-published_at"
    )

    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "category": category,
        "page_obj": page_obj,
        "posts": page_obj,
    }
    return render(request, "blog/category_posts.html", context)


def search(request):
    query = request.GET.get("q")
    posts = []

    if query:
        posts = (
            Post.objects.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(tags__name__icontains=query),
                status="published",
            )
            .distinct()
            .order_by("-published_at")
        )

    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "query": query,
        "page_obj": page_obj,
        "posts": page_obj,
    }
    return render(request, "blog/search_results.html", context)


def tag_posts(request, tag_slug):
    posts = Post.objects.filter(tags__slug=tag_slug, status="published").order_by(
        "-published_at"
    )
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "tag_slug": tag_slug,
        "page_obj": page_obj,
        "posts": page_obj,
    }
    return render(request, "blog/tag_posts.html", context)


def about(request):
    return render(request, "blog/about.html")


def contact(request):
    return render(request, "blog/contact.html")
