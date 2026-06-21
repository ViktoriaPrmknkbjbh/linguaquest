from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('about/', views.about_view, name='about'),
    path("pol_comfid/", views.pol_comfid, name="pol_comfid"),
    path("faq/", views.faq_view, name="faq"),
]