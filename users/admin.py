from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = ('email', 'ip_address', 'user')
    list_display_links = ('email', 'ip_address')