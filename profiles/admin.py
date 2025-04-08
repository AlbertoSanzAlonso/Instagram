from django.contrib import admin
from profiles.models import UserProfile, Follow


# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    resource_class = UserProfile
    list_display = ('user', 'birth_date')

@admin.register(Follow)   
class FollowAdmin(admin.ModelAdmin):
    resource_class = Follow
    list_display = ('follower', 'following', 'created_at')

