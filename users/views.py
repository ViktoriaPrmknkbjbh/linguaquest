from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from courses.models import LessonResult
from courses.models import Course, Lesson, Exercise, CourseComment, CourseAccessRequest, LessonResult
from courses.forms import CourseForm, LessonForm, ExerciseForm

from .forms import (
    UserRegisterForm,
    UserLoginForm,
    UserUpdateForm,
    UserProfileUpdateForm,
    RejectAccessRequestForm
)
from .models import UserProfile
from courses.models import Course, Lesson, CourseAccessRequest
from courses.forms import CourseForm, LessonForm
from achievements.models import UserAchievement


def register_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')

        return redirect('profile')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()

            login(request, user)

            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('profile')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {
        'form': form
    })


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')

        return redirect('profile')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, 'Вы успешно вошли в аккаунт.')

            if user.is_staff:
                return redirect('admin_dashboard')

            return redirect('profile')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {
        'form': form
    })


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('home')


@login_required
def profile_view(request):
    if request.user.is_staff:
        raise PermissionDenied

    public_courses = Course.objects.filter(is_public=True)

    approved_course_ids = CourseAccessRequest.objects.filter(
        user=request.user,
        status='approved'
    ).values_list('course_id', flat=True)

    approved_private_courses = Course.objects.filter(
        id__in=approved_course_ids,
        is_public=False
    )

    access_requests = CourseAccessRequest.objects.filter(
        user=request.user
    ).select_related('course').order_by('-updated_at')

    user_achievements = UserAchievement.objects.filter(
        user=request.user
    ).select_related('achievement').order_by('-received_at')

    available_courses = []

    for course in public_courses:
        available_courses.append(course)

    for course in approved_private_courses:
        available_courses.append(course)

    courses_progress = []
    courses_progress = [
        item for item in courses_progress
        if item["completed_lessons"] > 0 or item["progress_percent"] > 0
    ]

    for course in available_courses:
        total_lessons = course.lessons.count()

        completed_lessons = LessonResult.objects.filter(
            user=request.user,
            lesson__course=course,
            best_score__gte=50
        ).count()

        if total_lessons > 0:
            progress_percent = int((completed_lessons / total_lessons) * 100)
        else:
            progress_percent = 0

        courses_progress.append({
            'course': course,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress_percent': progress_percent
        })
    total_points = request.user.profile.total_points if hasattr(request.user, 'profile') else 0

    level = total_points // 100 + 1
    current_level_points = total_points % 100
    next_level_points = 100
    level_progress_percent = current_level_points
    streak_days = request.user.profile.streak_days
    return render(request, 'users/profile.html', {
        'public_courses': public_courses,
        'approved_private_courses': approved_private_courses,
        'access_requests': access_requests,
        'user_achievements': user_achievements,
        'courses_progress': courses_progress,
        'total_points': total_points,
        'level': level,
        'current_level_points': current_level_points,
        'next_level_points': next_level_points,
        'level_progress_percent': level_progress_percent,
        'streak_days': streak_days,
    })

def rating_view(request):
    profiles = UserProfile.objects.filter(
        user__is_staff=False
    ).select_related('user').order_by('-total_points', 'user__username')

    return render(request, 'users/rating.html', {
        'profiles': profiles
    })


@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        raise PermissionDenied

    courses = Course.objects.all().order_by('-created_at')

    pending_requests = CourseAccessRequest.objects.filter(
        status='pending'
    ).select_related('user', 'course').order_by('-created_at')

    approved_requests = CourseAccessRequest.objects.filter(
        status='approved'
    ).select_related('user', 'course').order_by('-updated_at')[:10]

    rejected_requests = CourseAccessRequest.objects.filter(
        status='rejected'
    ).select_related('user', 'course').order_by('-updated_at')[:10]

    return render(request, 'users/admin_dashboard.html', {
        'courses': courses,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests
    })


@login_required
def admin_course_create_view(request):
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Курс успешно создан.')
            return redirect('admin_dashboard')
    else:
        form = CourseForm()

    return render(request, 'users/admin_course_form.html', {
        'form': form,
        'page_title': 'Добавление курса',
        'button_text': 'Создать курс'
    })


@login_required
def admin_course_update_view(request, course_id):
    if not request.user.is_staff:
        raise PermissionDenied

    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)

        if form.is_valid():
            form.save()
            messages.success(request, 'Курс успешно обновлён.')
            return redirect('admin_dashboard')
    else:
        form = CourseForm(instance=course)

    return render(request, 'users/admin_course_form.html', {
        'form': form,
        'page_title': 'Редактирование курса',
        'button_text': 'Сохранить изменения'
    })


@login_required
def admin_course_delete_view(request, course_id):
    if not request.user.is_staff:
        raise PermissionDenied

    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Курс успешно удалён.')
        return redirect('admin_dashboard')

    return render(request, 'users/admin_course_confirm_delete.html', {
        'course': course
    })


@login_required
def admin_course_lessons_view(request, course_id):
    if not request.user.is_staff:
        raise PermissionDenied

    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()

    return render(request, 'users/admin_course_lessons.html', {
        'course': course,
        'lessons': lessons
    })


@login_required
def admin_lesson_create_view(request, course_id):
    if not request.user.is_staff:
        raise PermissionDenied

    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = LessonForm(request.POST)

        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()

            messages.success(request, 'Урок успешно создан.')
            return redirect('admin_course_lessons', course_id=course.id)
    else:
        form = LessonForm()

    return render(request, 'users/admin_lesson_form.html', {
        'form': form,
        'course': course,
        'page_title': 'Добавление урока',
        'button_text': 'Создать урок'
    })


@login_required
def admin_lesson_update_view(request, course_id, lesson_id):
    if not request.user.is_staff:
        raise PermissionDenied

    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)

        if form.is_valid():
            form.save()
            messages.success(request, 'Урок успешно обновлён.')
            return redirect('admin_course_lessons', course_id=course.id)
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'users/admin_lesson_form.html', {
        'form': form,
        'course': course,
        'lesson': lesson,
        'page_title': 'Редактирование урока',
        'button_text': 'Сохранить изменения'
    })


@login_required
def admin_lesson_delete_view(request, course_id, lesson_id):
    if not request.user.is_staff:
        raise PermissionDenied

    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    if request.method == 'POST':
        lesson.delete()
        messages.success(request, 'Урок успешно удалён.')
        return redirect('admin_course_lessons', course_id=course.id)

    return render(request, 'users/admin_lesson_confirm_delete.html', {
        'course': course,
        'lesson': lesson
    })


@login_required
def admin_lesson_exercises_view(request, course_id, lesson_id):
    if not request.user.is_staff:
        raise PermissionDenied

    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    exercises = lesson.exercises.all()

    return render(request, 'users/admin_lesson_exercises.html', {
        'course': course,
        'lesson': lesson,
        'exercises': exercises
    })


@login_required
def admin_exercise_create_view(request, course_id, lesson_id):
    if not request.user.is_staff:
        raise PermissionDenied

    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    if request.method == 'POST':
        form = ExerciseForm(request.POST)

        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.lesson = lesson
            exercise.save()

            messages.success(request, 'Упражнение успешно создано.')
            return redirect(
                'admin_lesson_exercises',
                course_id=course.id,
                lesson_id=lesson.id
            )
    else:
        form = ExerciseForm()

    return render(request, 'users/admin_exercise_form.html', {
        'form': form,
        'course': course,
        'lesson': lesson,
        'page_title': 'Добавление упражнения',
        'button_text': 'Создать упражнение'
    })


@login_required
def admin_exercise_update_view(request, course_id, lesson_id, exercise_id):
    if not request.user.is_staff:
        raise PermissionDenied

    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    exercise = get_object_or_404(Exercise, id=exercise_id, lesson=lesson)

    if request.method == 'POST':
        form = ExerciseForm(request.POST, instance=exercise)

        if form.is_valid():
            form.save()
            messages.success(request, 'Упражнение успешно обновлено.')
            return redirect(
                'admin_lesson_exercises',
                course_id=course.id,
                lesson_id=lesson.id
            )
    else:
        form = ExerciseForm(instance=exercise)

    return render(request, 'users/admin_exercise_form.html', {
        'form': form,
        'course': course,
        'lesson': lesson,
        'exercise': exercise,
        'page_title': 'Редактирование упражнения',
        'button_text': 'Сохранить изменения'
    })


@login_required
def admin_exercise_delete_view(request, course_id, lesson_id, exercise_id):
    if not request.user.is_staff:
        raise PermissionDenied

    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    exercise = get_object_or_404(Exercise, id=exercise_id, lesson=lesson)

    if request.method == 'POST':
        exercise.delete()
        messages.success(request, 'Упражнение успешно удалено.')
        return redirect(
            'admin_lesson_exercises',
            course_id=course.id,
            lesson_id=lesson.id
        )

    return render(request, 'users/admin_exercise_confirm_delete.html', {
        'course': course,
        'lesson': lesson,
        'exercise': exercise
    })


@login_required
def approve_access_request_view(request, request_id):
    if not request.user.is_staff:
        raise PermissionDenied

    access_request = get_object_or_404(CourseAccessRequest, id=request_id)

    if request.method == 'POST':
        access_request.status = 'approved'
        access_request.admin_comment = ''
        access_request.save()

        messages.success(
            request,
            f'Заявка пользователя {access_request.user.username} одобрена.'
        )

    return redirect('admin_dashboard')


@login_required
def reject_access_request_view(request, request_id):
    if not request.user.is_staff:
        raise PermissionDenied

    access_request = get_object_or_404(CourseAccessRequest, id=request_id)

    if request.method == 'POST':
        form = RejectAccessRequestForm(request.POST)

        if form.is_valid():
            access_request.status = 'rejected'
            access_request.admin_comment = form.cleaned_data['admin_comment']
            access_request.save()

            messages.success(
                request,
                f'Заявка пользователя {access_request.user.username} отклонена.'
            )

            return redirect('admin_dashboard')
    else:
        form = RejectAccessRequestForm()

    return render(request, 'users/reject_access_request.html', {
        'form': form,
        'access_request': access_request
    })


@login_required
def admin_comments_view(request):
    if not request.user.is_staff:
        raise PermissionDenied

    comments = CourseComment.objects.select_related(
        'user',
        'course'
    ).order_by('-created_at')

    return render(request, 'users/admin_comments.html', {
        'comments': comments
    })


@login_required
def admin_comment_delete_view(request, comment_id):
    if not request.user.is_staff:
        raise PermissionDenied

    comment = get_object_or_404(CourseComment, id=comment_id)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Комментарий успешно удалён.')
        return redirect('admin_comments')

    return render(request, 'users/admin_comment_confirm_delete.html', {
        'comment': comment
    })

@login_required
def profile_settings_view(request):
    if request.user.is_staff:
        raise PermissionDenied

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Данные профиля успешно обновлены.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=profile)

    return render(request, 'users/profile_settings.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })