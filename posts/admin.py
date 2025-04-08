from django.contrib import admin
from posts.models import Post, Comment

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    resource_class = Post
    list_display = ('user', 'created_at', 'caption')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    resource_class = Comment
    list_display = ('post', 'user', 'created_at', 'text')