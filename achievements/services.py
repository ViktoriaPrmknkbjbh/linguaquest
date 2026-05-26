from achievements.models import Achievement, UserAchievement
from courses.models import LessonResult


def give_achievement(user, code):
    achievement = Achievement.objects.filter(code=code).first()

    if not achievement:
        return None

    user_achievement, created = UserAchievement.objects.get_or_create(
        user=user,
        achievement=achievement
    )

    if created:
        return user_achievement

    return None


def check_lesson_achievements(user, lesson, score):
    if user.is_staff:
        return []

    new_achievements = []

    completed_lessons_count = LessonResult.objects.filter(
        user=user,
        best_score__gte=50
    ).count()

    perfect_lessons_count = LessonResult.objects.filter(
        user=user,
        best_score=100
    ).count()

    if completed_lessons_count >= 1:
        achievement = give_achievement(user, 'first_lesson')

        if achievement:
            new_achievements.append(achievement)

    if score == 100:
        achievement = give_achievement(user, 'perfect_lesson')

        if achievement:
            new_achievements.append(achievement)

    if perfect_lessons_count >= 5:
        achievement = give_achievement(user, 'five_perfect_lessons')

        if achievement:
            new_achievements.append(achievement)

    return new_achievements