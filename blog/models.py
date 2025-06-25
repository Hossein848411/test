from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته بندی")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="اسلاگ")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category_posts", kwargs={"slug": self.slug})


class Post(models.Model):
    STATUS_CHOICES = [("draft", "پیش نویس"), ("published", "منتشر شده")]
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="اسلاگ")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="نویسنده")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="دسته‌بندی"
    )
    content = RichTextUploadingField(verbose_name="محتوا")
    excerpt = models.TextField(max_length=300, blank=True, verbose_name="خلاصه")
    featured_image = models.ImageField(
        upload_to="posts/", blank=True, null=True, verbose_name="تصویر شاخص"
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft", verbose_name="وضعیت"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    published_at = models.DateTimeField(
        blank=True, null=True, verbose_name="تاریخ انتشار"
    )
    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")

    tags = TaggableManager(verbose_name="برچسب‌ها", blank=True)

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="پست"
    )
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    content = models.TextField(verbose_name="محتوای کامنت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="replies",
        verbose_name="والد",
    )

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"کامنت {self.name} برای {self.post.title}"
