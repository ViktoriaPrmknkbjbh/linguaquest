from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )

    total_points = models.PositiveIntegerField(
        default=0,
        verbose_name='Общее количество баллов'
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    streak_days = models.PositiveIntegerField(
        default=0,
        verbose_name='Серия дней'
    )

    last_activity_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата последней активности'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания профиля'
    )

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
