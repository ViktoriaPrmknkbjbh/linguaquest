from django.test import TestCase
from django.contrib.auth.models import User

from courses.models import Course, Lesson, Exercise, LessonResult


class LinguaQuestTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        self.course = Course.objects.create(
            title="English A1",
            description="Курс английского языка",
            level="A1"
        )

        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Lesson 1",
            content="Test lesson content",
            order=1,
            points_reward=10
        )

        self.exercise = Exercise.objects.create(
            lesson=self.lesson,
            question="Choose correct answer",
            exercise_type="choice",
            option_1="Hello",
            option_2="Bye",
            option_3="Cat",
            option_4="Dog",
            correct_answer="Hello",
            order=1
        )

    def test_01_user_created(self):
        self.assertEqual(self.user.username, "testuser")

    def test_02_user_password_check(self):
        self.assertTrue(self.user.check_password("testpassword123"))

    def test_03_course_created(self):
        self.assertEqual(self.course.title, "English A1")

    def test_04_course_level(self):
        self.assertEqual(self.course.level, "A1")

    def test_05_course_description(self):
        self.assertEqual(self.course.description, "Курс английского языка")

    def test_06_lesson_created(self):
        self.assertEqual(self.lesson.title, "Lesson 1")

    def test_07_lesson_belongs_to_course(self):
        self.assertEqual(self.lesson.course, self.course)

    def test_08_lesson_order(self):
        self.assertEqual(self.lesson.order, 1)

    def test_09_lesson_points_reward(self):
        self.assertEqual(self.lesson.points_reward, 10)

    def test_10_exercise_created(self):
        self.assertEqual(self.exercise.question, "Choose correct answer")

    def test_11_exercise_belongs_to_lesson(self):
        self.assertEqual(self.exercise.lesson, self.lesson)

    def test_12_exercise_type(self):
        self.assertEqual(self.exercise.exercise_type, "choice")

    def test_13_exercise_correct_answer(self):
        self.assertEqual(self.exercise.correct_answer, "Hello")

    def test_14_exercise_options(self):
        self.assertEqual(self.exercise.option_1, "Hello")
        self.assertEqual(self.exercise.option_2, "Bye")
        self.assertEqual(self.exercise.option_3, "Cat")
        self.assertEqual(self.exercise.option_4, "Dog")

    def test_15_lesson_result_created(self):
        result = LessonResult.objects.create(
            user=self.user,
            lesson=self.lesson,
            best_score=100,
            points_earned=10
        )

        self.assertEqual(result.best_score, 100)

    def test_16_lesson_result_points(self):
        result = LessonResult.objects.create(
            user=self.user,
            lesson=self.lesson,
            best_score=80,
            points_earned=10
        )

        self.assertEqual(result.points_earned, 10)