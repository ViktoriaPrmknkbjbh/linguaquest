from django import forms

from .models import Course, Lesson, Exercise, CourseComment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'level',
            'category',
            'is_public',
            'image',
        ]

        labels = {
            'title': 'Название курса',
            'description': 'Описание курса',
            'level': 'Уровень',
            'category': 'Категория',
            'is_public': 'Открытый курс',
            'image': 'Изображение курса',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название курса'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание курса',
                'rows': 5
            }),
            'level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            'title',
            'content',
            'order',
            'points_reward',
        ]

        labels = {
            'title': 'Название урока',
            'content': 'Материал урока',
            'order': 'Порядковый номер',
            'points_reward': 'Баллы за прохождение',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название урока'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите материал урока',
                'rows': 8
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'points_reward': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
        }


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = [
            'exercise_type',
            'question',
            'source_text',
            'option_1',
            'option_2',
            'option_3',
            'option_4',
            'correct_option',
            'correct_answer',
            'words_for_ordering',
            'explanation',
            'order',
        ]

        labels = {
            'exercise_type': 'Тип упражнения',
            'question': 'Задание',
            'source_text': 'Исходный текст',
            'option_1': 'Вариант 1',
            'option_2': 'Вариант 2',
            'option_3': 'Вариант 3',
            'option_4': 'Вариант 4',
            'correct_option': 'Правильный вариант',
            'correct_answer': 'Правильный ответ',
            'words_for_ordering': 'Слова для сборки предложения',
            'explanation': 'Объяснение после ответа',
            'order': 'Порядковый номер',
        }

        widgets = {
            'exercise_type': forms.Select(attrs={'class': 'form-control'}),

            'question': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Выберите правильный перевод слова "cat"',
                'rows': 3
            }),

            'source_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Например: I ___ a student. Или фраза для перевода',
                'rows': 3
            }),

            'option_1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вариант ответа 1'
            }),

            'option_2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вариант ответа 2'
            }),

            'option_3': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вариант ответа 3'
            }),

            'option_4': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вариант ответа 4'
            }),

            'correct_option': forms.Select(attrs={
                'class': 'form-control'
            }),

            'correct_answer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: I am a student'
            }),

            'words_for_ordering': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: I am a student'
            }),

            'explanation': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Объяснение правильного ответа',
                'rows': 4
            }),

            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
        }


class CourseCommentForm(forms.ModelForm):
    class Meta:
        model = CourseComment
        fields = ['text']

        labels = {
            'text': 'Комментарий'
        }

        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Поделитесь мнением о курсе',
                'rows': 4
            })
        }