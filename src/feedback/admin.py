from django.contrib import admin
from .models import Comment, Playlist,Like

admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Playlist)
