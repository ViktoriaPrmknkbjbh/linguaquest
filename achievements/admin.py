from django.contrib import admin

from .models import Achievement, UserAchievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'code')
    search_fields = ('title', 'description', 'code')


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'received_at')
    list_filter = ('achievement', 'received_at')
    search_fields = ('user__username', 'achievement__title')