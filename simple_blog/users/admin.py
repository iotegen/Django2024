from django.contrib import admin

# Register your models here.
from .models import Profile,Follow
admin.site.register(Profile)
admin.site.register(Follow)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'User', 'Bio', 'ProfilePicture')
    search_fields = ('Bio',)

class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following')
    search_fields = ('id',)
