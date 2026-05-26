from django.urls import path

from . import views


urlpatterns = [
    path('', views.course_list_view, name='course_list'),
    path('<int:course_id>/', views.course_detail_view, name='course_detail'),

    path(
        '<int:course_id>/lessons/<int:lesson_id>/',
        views.lesson_detail_view,
        name='lesson_detail'
    ),

    path(
        '<int:course_id>/lessons/<int:lesson_id>/start/',
        views.start_lesson_exercises_view,
        name='start_lesson_exercises'
    ),

    path(
        '<int:course_id>/lessons/<int:lesson_id>/exercises/<int:exercise_number>/',
        views.lesson_exercise_view,
        name='lesson_exercise'
    ),

    path(
        '<int:course_id>/lessons/<int:lesson_id>/exercises/<int:exercise_number>/feedback/',
        views.lesson_exercise_feedback_view,
        name='lesson_exercise_feedback'
    ),

    path(
        '<int:course_id>/lessons/<int:lesson_id>/result/',
        views.lesson_result_view,
        name='lesson_result'
    ),

    path(
        '<int:course_id>/request-access/',
        views.request_course_access_view,
        name='request_course_access'
    ),
]