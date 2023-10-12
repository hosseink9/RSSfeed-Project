from django.contrib import admin
from .models import User, Notification,NotificationInfo


admin.site.register(User)
admin.site.register(NotificationInfo)
admin.site.register(Notification)
