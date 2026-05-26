
from django.db import models
from django.contrib.auth.models import User


class Achievement(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Название достижения'
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    sticker = models.ImageField(
        upload_to='achievements/',
        blank=True,
        null=True,
        verbose_name='Стикер'
    )

    code = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Код достижения'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'


class UserAchievement(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='achievements',
        verbose_name='Пользователь'
    )

    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Достижение'
    )

    received_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата получения'
    )

    def __str__(self):
        return f'{self.user.username} — {self.achievement.title}'

    class Meta:
        verbose_name = 'Достижение пользователя'
        verbose_name_plural = 'Достижения пользователей'
        unique_together = ['user', 'achievement']