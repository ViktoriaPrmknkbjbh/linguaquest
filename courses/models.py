from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    LEVEL_CHOICES = [
        ('A1', 'Начальный A1'),
        ('A2', 'Элементарный A2'),
        ('B1', 'Средний B1'),
        ('B2', 'Выше среднего B2'),
        ('C1', 'Продвинутый C1'),
    ]

    CATEGORY_CHOICES = [
        ('general', 'Общий английский'),
        ('it', 'Английский в IT'),
        ('business', 'Бизнес английский'),
        ('travel', 'Английский для путешествий'),
    ]

    title = models.CharField(
        max_length=255,
        verbose_name='Название курса'
    )

    description = models.TextField(
        verbose_name='Описание курса'
    )

    level = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        verbose_name='Уровень'
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='general',
        verbose_name='Категория'
    )

    is_public = models.BooleanField(
        default=True,
        verbose_name='Открытый курс'
    )

    image = models.ImageField(
        upload_to='courses/',
        blank=True,
        null=True,
        verbose_name='Изображение курса'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )

    title = models.CharField(
        max_length=255,
        verbose_name='Название урока'
    )

    content = models.TextField(
        verbose_name='Материал урока'
    )

    order = models.PositiveIntegerField(
        verbose_name='Порядковый номер'
    )

    points_reward = models.PositiveIntegerField(
        default=10,
        verbose_name='Баллы за прохождение'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'{self.course.title} — {self.title}'

    class Meta:
        ordering = ['order']
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        unique_together = ['course', 'order']


class Exercise(models.Model):
    EXERCISE_TYPE_CHOICES = [
        ('choice', 'Выбор одного ответа'),
        ('text_input', 'Ввод ответа текстом'),
        ('translate', 'Перевод фразы'),
        ('fill_gap', 'Заполнение пропуска'),
        ('order_words', 'Сбор предложения из слов'),
    ]

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='exercises',
        verbose_name='Урок'
    )

    exercise_type = models.CharField(
        max_length=30,
        choices=EXERCISE_TYPE_CHOICES,
        verbose_name='Тип упражнения'
    )

    question = models.TextField(
        verbose_name='Задание'
    )

    source_text = models.TextField(
        blank=True,
        verbose_name='Исходный текст'
    )

    option_1 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Вариант 1'
    )

    option_2 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Вариант 2'
    )

    option_3 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Вариант 3'
    )

    option_4 = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Вариант 4'
    )

    correct_option = models.PositiveSmallIntegerField(
        choices=[
            (1, 'Вариант 1'),
            (2, 'Вариант 2'),
            (3, 'Вариант 3'),
            (4, 'Вариант 4'),
        ],
        blank=True,
        null=True,
        verbose_name='Правильный вариант'
    )

    correct_answer = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Правильный ответ'
    )

    words_for_ordering = models.TextField(
        blank=True,
        verbose_name='Слова для сборки предложения'
    )

    explanation = models.TextField(
        blank=True,
        verbose_name='Объяснение после ответа'
    )

    order = models.PositiveIntegerField(
        default=1,
        verbose_name='Порядок упражнения'
    )

    def __str__(self):
        return f'{self.lesson.title} — {self.get_exercise_type_display()}'

    class Meta:
        ordering = ['order']
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'


class CourseComment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_comments',
        verbose_name='Пользователь'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Курс'
    )

    text = models.TextField(
        verbose_name='Комментарий'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f'{self.user.username} — {self.course.title}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий к курсу'
        verbose_name_plural = 'Комментарии к курсам'


class CourseAccessRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_access_requests',
        verbose_name='Пользователь'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='access_requests',
        verbose_name='Курс'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус'
    )

    admin_comment = models.TextField(
        blank=True,
        verbose_name='Комментарий администратора'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата заявки'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    def __str__(self):
        return f'{self.user.username} — {self.course.title} — {self.get_status_display()}'

    class Meta:
        verbose_name = 'Заявка на доступ к курсу'
        verbose_name_plural = 'Заявки на доступ к курсам'
        unique_together = ['user', 'course']

class LessonResult(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lesson_results',
        verbose_name='Пользователь'
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='Урок'
    )

    best_score = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Лучший результат в процентах'
    )

    points_earned = models.PositiveIntegerField(
        default=0,
        verbose_name='Полученные баллы'
    )

    completed_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего прохождения'
    )

    def is_passed(self):
        return self.best_score >= 50

    def __str__(self):
        return f'{self.user.username} — {self.lesson.title} — {self.best_score}%'

    class Meta:
        unique_together = ['user', 'lesson']
        verbose_name = 'Результат урока'
        verbose_name_plural = 'Результаты уроков'