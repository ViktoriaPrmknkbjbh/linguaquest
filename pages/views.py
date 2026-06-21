from django.shortcuts import render

from courses.models import Course


def home_view(request):
    beginner_courses = Course.objects.filter(
        level="A1",
        is_deleted=False
    ).order_by("title")

    return render(request, "pages/index.html", {
        "beginner_courses": beginner_courses,
    })


def about_view(request):
    return render(request, "pages/about.html")

def faq_view(request):
    return render(request, "pages/faq.html")


def pol_comfid(request):
    return render(request, "pages/pol_comfid.html")


def custom_403_view(request, exception=None):
    return render(request, "errors/403.html", status=403)


def custom_404_view(request, exception=None):
    return render(request, "errors/404.html", status=404)


def custom_500_view(request):
    return render(request, "errors/500.html", status=500)