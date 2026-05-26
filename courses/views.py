from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from achievements.services import check_lesson_achievements
from .forms import CourseCommentForm
from .models import Course, Lesson, Exercise, CourseAccessRequest, LessonResult
from courses.models import LessonResult
from datetime import date, timedelta
from users.models import UserProfile
from django.core.paginator import Paginator


def user_has_course_access(user, course):
    if course.is_public:
        return True

    if not user.is_authenticated:
        return False

    if user.is_staff:
        return True

    return CourseAccessRequest.objects.filter(
        user=user,
        course=course,
        status='approved'
    ).exists()


def is_lesson_unlocked(user, lesson):
    if not user.is_authenticated:
        return False

    if user.is_staff:
        return True

    if lesson.order == 1:
        return True

    previous_lesson = Lesson.objects.filter(
        course=lesson.course,
        order=lesson.order - 1
    ).first()

    if not previous_lesson:
        return True

    return LessonResult.objects.filter(
        user=user,
        lesson=previous_lesson,
        best_score__gte=50
    ).exists()


def normalize_answer(answer):
    if answer is None:
        return ''

    return answer.strip().lower()


def get_correct_answer_text(exercise):
    if exercise.exercise_type == 'choice':
        options = {
            1: exercise.option_1,
            2: exercise.option_2,
            3: exercise.option_3,
            4: exercise.option_4,
        }

        return options.get(exercise.correct_option, '')

    return exercise.correct_answer


def check_exercise_answer(exercise, user_answer):
    if exercise.exercise_type == 'choice':
        try:
            return int(user_answer) == exercise.correct_option
        except (TypeError, ValueError):
            return False

    return normalize_answer(user_answer) == normalize_answer(exercise.correct_answer)

def course_list_view(request):
    courses = Course.objects.all()

    search_query = request.GET.get('q', '')
    selected_level = request.GET.get('level', '')
    selected_sort = request.GET.get('sort', 'new')

    if search_query:
        courses = courses.filter(title__icontains=search_query)

    if selected_level:
        courses = courses.filter(level=selected_level)

    if selected_sort == 'title':
        courses = courses.order_by('title')
    else:
        courses = courses.order_by('-created_at')

    return render(request, 'courses/course_list.html', {
        'courses': courses,
        'search_query': search_query,
        'selected_level': selected_level,
        'selected_sort': selected_sort,
        'levels': Course.LEVEL_CHOICES
    })


from django.shortcuts import render
from courses.models import Course



def course_detail_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    has_access = user_has_course_access(request.user, course)
    access_request = None

    all_lessons = course.lessons.all().order_by('order')

    paginator = Paginator(all_lessons, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated and not request.user.is_staff:
        access_request = CourseAccessRequest.objects.filter(
            user=request.user,
            course=course
        ).first()

    if request.method == 'POST':
        if not request.user.is_authenticated or request.user.is_staff:
            raise PermissionDenied

        comment_form = CourseCommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.course = course
            comment.save()

            messages.success(request, 'Комментарий успешно добавлен.')
            return redirect('course_detail', course_id=course.id)
    else:
        comment_form = CourseCommentForm()

    lesson_data = []

    for lesson in page_obj:
        result = None
        unlocked = False

        if request.user.is_authenticated:
            result = LessonResult.objects.filter(
                user=request.user,
                lesson=lesson
            ).first()

            unlocked = is_lesson_unlocked(request.user, lesson)

        lesson_data.append({
            'lesson': lesson,
            'result': result,
            'unlocked': unlocked
        })

    comments = course.comments.select_related('user').all()

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'page_obj': page_obj,
        'lesson_data': lesson_data,
        'has_access': has_access,
        'access_request': access_request,
        'comments': comments,
        'comment_form': comment_form
    })


def lesson_detail_view(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    if not request.user.is_authenticated:
        raise PermissionDenied

    if not user_has_course_access(request.user, course):
        raise PermissionDenied

    if not is_lesson_unlocked(request.user, lesson):
        raise PermissionDenied

    result = None

    if not request.user.is_staff:
        result = LessonResult.objects.filter(
            user=request.user,
            lesson=lesson
        ).first()

    exercises_count = lesson.exercises.count()

    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'result': result,
        'exercises_count': exercises_count
    })


def start_lesson_exercises_view(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    if not request.user.is_authenticated:
        raise PermissionDenied

    if not user_has_course_access(request.user, course):
        raise PermissionDenied

    if not is_lesson_unlocked(request.user, lesson):
        raise PermissionDenied

    exercises = lesson.exercises.all()

    if not exercises.exists():
        messages.error(request, 'В этом уроке пока нет упражнений.')
        return redirect('lesson_detail', course_id=course.id, lesson_id=lesson.id)

    session_key = f'lesson_{lesson.id}_answers'

    request.session[session_key] = {
        'correct_count': 0,
        'answered_exercises': [],
        'last_answer': None
    }

    return redirect(
        'lesson_exercise',
        course_id=course.id,
        lesson_id=lesson.id,
        exercise_number=1
    )


def lesson_exercise_view(request, course_id, lesson_id, exercise_number):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    if not request.user.is_authenticated:
        raise PermissionDenied

    if not user_has_course_access(request.user, course):
        raise PermissionDenied

    if not is_lesson_unlocked(request.user, lesson):
        raise PermissionDenied

    exercises = list(lesson.exercises.all())

    if exercise_number < 1 or exercise_number > len(exercises):
        raise PermissionDenied

    exercise = exercises[exercise_number - 1]

    session_key = f'lesson_{lesson.id}_answers'

    if session_key not in request.session:
        request.session[session_key] = {
            'correct_count': 0,
            'answered_exercises': [],
            'last_answer': None
        }

    session_data = request.session[session_key]

    if request.method == 'POST':
        user_answer = request.POST.get('answer')
        is_correct = check_exercise_answer(exercise, user_answer)

        if exercise.id not in session_data['answered_exercises']:
            session_data['answered_exercises'].append(exercise.id)

            if is_correct:
                session_data['correct_count'] += 1

        session_data['last_answer'] = {
            'exercise_id': exercise.id,
            'exercise_number': exercise_number,
            'user_answer': user_answer,
            'is_correct': is_correct
        }

        request.session[session_key] = session_data
        request.session.modified = True

        return redirect(
            'lesson_exercise_feedback',
            course_id=course.id,
            lesson_id=lesson.id,
            exercise_number=exercise_number
        )

    progress_percent = int((exercise_number / len(exercises)) * 100)

    return render(request, 'courses/lesson_exercise.html', {
        'course': course,
        'lesson': lesson,
        'exercise': exercise,
        'exercise_number': exercise_number,
        'exercises_count': len(exercises),
        'progress_percent': progress_percent
    })


def lesson_exercise_feedback_view(request, course_id, lesson_id, exercise_number):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    if not request.user.is_authenticated:
        raise PermissionDenied

    if not user_has_course_access(request.user, course):
        raise PermissionDenied

    if not is_lesson_unlocked(request.user, lesson):
        raise PermissionDenied

    exercises = list(lesson.exercises.all())

    if exercise_number < 1 or exercise_number > len(exercises):
        raise PermissionDenied

    exercise = exercises[exercise_number - 1]

    session_key = f'lesson_{lesson.id}_answers'
    session_data = request.session.get(session_key)

    if not session_data or not session_data.get('last_answer'):
        return redirect(
            'lesson_exercise',
            course_id=course.id,
            lesson_id=lesson.id,
            exercise_number=exercise_number
        )

    last_answer = session_data['last_answer']

    if last_answer.get('exercise_id') != exercise.id:
        return redirect(
            'lesson_exercise',
            course_id=course.id,
            lesson_id=lesson.id,
            exercise_number=exercise_number
        )

    next_exercise_number = exercise_number + 1
    has_next_exercise = next_exercise_number <= len(exercises)

    return render(request, 'courses/lesson_exercise_feedback.html', {
        'course': course,
        'lesson': lesson,
        'exercise': exercise,
        'exercise_number': exercise_number,
        'exercises_count': len(exercises),
        'user_answer': last_answer.get('user_answer'),
        'is_correct': last_answer.get('is_correct'),
        'correct_answer': get_correct_answer_text(exercise),
        'has_next_exercise': has_next_exercise,
        'next_exercise_number': next_exercise_number
    })


def lesson_result_view(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    if not request.user.is_authenticated:
        raise PermissionDenied

    if not user_has_course_access(request.user, course):
        raise PermissionDenied

    if not is_lesson_unlocked(request.user, lesson):
        raise PermissionDenied

    exercises_count = lesson.exercises.count()

    if exercises_count == 0:
        messages.error(request, 'В этом уроке пока нет упражнений.')
        return redirect('lesson_detail', course_id=course.id, lesson_id=lesson.id)

    session_key = f'lesson_{lesson.id}_answers'
    session_data = request.session.get(session_key)

    if not session_data:
        return redirect('lesson_detail', course_id=course.id, lesson_id=lesson.id)

    correct_count = session_data.get('correct_count', 0)
    score = int((correct_count / exercises_count) * 100)

    result = None
    points_added = 0
    old_best_score = 0
    new_achievements = []

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    today = date.today()

    if profile.last_activity_date == today:
        pass
    elif profile.last_activity_date == today - timedelta(days=1):
        profile.streak_days += 1
    else:
        profile.streak_days = 1

    profile.last_activity_date = today
    profile.save()

    if not request.user.is_staff:
        result, created = LessonResult.objects.get_or_create(
            user=request.user,
            lesson=lesson,
            defaults={
                'best_score': 0,
                'points_earned': 0
            }
        )

        old_best_score = result.best_score

        if score > result.best_score:
            result.best_score = score

            if score >= 50 and result.points_earned == 0:
                result.points_earned = lesson.points_reward
                points_added = lesson.points_reward

                profile.total_points += lesson.points_reward
                profile.save()

            result.save()

            new_achievements = check_lesson_achievements(
                request.user,
                lesson,
                score
            )

    if session_key in request.session:
        del request.session[session_key]

    return render(request, 'courses/lesson_result.html', {
        'course': course,
        'lesson': lesson,
        'correct_count': correct_count,
        'exercises_count': exercises_count,
        'score': score,
        'result': result,
        'points_added': points_added,
        'old_best_score': old_best_score,
        'new_achievements': new_achievements
    })


def request_course_access_view(request, course_id):
    if not request.user.is_authenticated:
        raise PermissionDenied

    if request.user.is_staff:
        raise PermissionDenied

    course = get_object_or_404(Course, id=course_id)

    if course.is_public:
        return render(request, 'courses/access_not_required.html', {
            'course': course
        })

    CourseAccessRequest.objects.update_or_create(
        user=request.user,
        course=course,
        defaults={
            'status': 'pending',
            'admin_comment': ''
        }
    )

    return render(request, 'courses/access_request_sent.html', {
        'course': course
    })