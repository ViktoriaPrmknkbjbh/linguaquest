from django.contrib import admin

from .models import Course, Lesson, Exercise, CourseComment, CourseAccessRequest


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'category', 'is_public', 'created_at')
    list_filter = ('level', 'category', 'is_public', 'created_at')
    search_fields = ('title', 'description')
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'points_reward', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('course', 'order')
    inlines = [ExerciseInline]


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'exercise_type', 'question', 'order')
    list_filter = ('exercise_type', 'lesson__course')
    search_fields = ('question', 'correct_answer')
    ordering = ('lesson', 'order')


@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('user__username', 'course__title', 'text')


@admin.register(CourseAccessRequest)
class CourseAccessRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'course', 'created_at')
    search_fields = ('user__username', 'course__title', 'admin_comment')