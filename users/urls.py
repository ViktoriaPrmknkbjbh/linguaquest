from django.urls import path

from . import views


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/settings/', views.profile_settings_view, name='profile_settings'),
    path('rating/', views.rating_view, name='rating'),

    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),

    path(
        'admin-dashboard/courses/create/',
        views.admin_course_create_view,
        name='admin_course_create'
    ),

    path(
        'admin-dashboard/courses/<int:course_id>/edit/',
        views.admin_course_update_view,
        name='admin_course_update'
    ),

    path(
        'admin-dashboard/courses/<int:course_id>/delete/',
        views.admin_course_delete_view,
        name='admin_course_delete'
    ),

    path(
        'admin-dashboard/courses/<int:course_id>/lessons/',
        views.admin_course_lessons_view,
        name='admin_course_lessons'
    ),

    path(
        'admin-dashboard/courses/<int:course_id>/lessons/create/',
        views.admin_lesson_create_view,
        name='admin_lesson_create'
    ),

    path(
        'admin-dashboard/courses/<int:course_id>/lessons/<int:lesson_id>/edit/',
        views.admin_lesson_update_view,
        name='admin_lesson_update'
    ),

    path(
        'admin-dashboard/courses/<int:course_id>/lessons/<int:lesson_id>/delete/',
        views.admin_lesson_delete_view,
        name='admin_lesson_delete'
    ),

    path(
        'admin-dashboard/courses/<int:course_id>/lessons/<int:lesson_id>/exercises/',
        views.admin_lesson_exercises_view,
        name='admin_lesson_exercises'
    ),

    path(
        'admin-dashboard/courses/<int:course_id>/lessons/<int:lesson_id>/exercises/create/',
        views.admin_exercise_create_view,
        name='admin_exercise_create'
    ),

    path(
        'admin-dashboard/courses/<int:course_id>/lessons/<int:lesson_id>/exercises/<int:exercise_id>/edit/',
        views.admin_exercise_update_view,
        name='admin_exercise_update'
    ),

    path(
        'admin-dashboard/courses/<int:course_id>/lessons/<int:lesson_id>/exercises/<int:exercise_id>/delete/',
        views.admin_exercise_delete_view,
        name='admin_exercise_delete'
    ),

    path(
        'admin-dashboard/comments/',
        views.admin_comments_view,
        name='admin_comments'
    ),

    path(
        'admin-dashboard/comments/<int:comment_id>/delete/',
        views.admin_comment_delete_view,
        name='admin_comment_delete'
    ),

    path(
        'access-requests/<int:request_id>/approve/',
        views.approve_access_request_view,
        name='approve_access_request'
    ),

    path(
        'access-requests/<int:request_id>/reject/',
        views.reject_access_request_view,
        name='reject_access_request'
    ),
]