from django.urls import path, re_path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/", views.post_list, name="post_list"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("category/<slug:slug>/", views.category_posts, name="category_posts"),
    re_path(
        r"^tag/(?P<tag_slug>[\w\-\u0600-\u06FF]+)/$", views.tag_posts, name="tag_posts"
    ),  # پشتیبانی از فارسی
    path("search/", views.search, name="search"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
