from django.contrib import admin
from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "created_at"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "status", "created_at", "views"]
    list_filter = ["status", "category", "created_at", "author"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    ordering = ["-created_at"]

    fieldsets = (
        ("اطلاعات اصلی", {"fields": ("title", "slug", "author", "category")}),
        ("محتوا", {"fields": ("content", "excerpt", "featured_image")}),
        ("تنظیمات انتشار", {"fields": ("status", "tags")}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "post", "created_at", "is_approved"]
    list_filter = ["is_approved", "created_at"]
    search_fields = ["name", "email", "content"]
    actions = ["approve_comments", "disapprove_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    approve_comments.short_description = "تایید کامنت‌های انتخاب شده"

    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)

    disapprove_comments.short_description = "رد کامنت‌های انتخاب شده"
