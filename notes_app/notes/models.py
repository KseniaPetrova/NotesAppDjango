from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Note(models.Model):
    """
       Модель заметки.

       Эта модель представляет заметку, содержащую заголовок,
       основное содержание, даты создания и редактирования, а также
       ссылку на пользователя - автора заметки.

       Атрибуты:
           title (str, optional): Заголовок заметки, который может быть пустым.
           content (str): Содержимое заметки.
           created_at (datetime): Дата и время создания заметки, автоматически устанавливается при создании.
           updated_at (datetime): Дата и время последнего редактирования заметки, обновляется при каждом изменении.
           author (User): Ссылка на пользователя, который является автором заметки.
    """

    title = models.CharField(max_length=200, blank=True, null=True)  # Заголовок не обязателен
    content = models.TextField()  # Основной текст
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата редактирования
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Владелец заметки

    def __str__(self):
        """
            Строковое представление заметки.

            Возвращает заголовок заметки, если он есть,
            иначе возвращает первые 80 символов содержания.

            Возвращает:
                str: Заголовок заметки или первые 80 символов содержания.
        """
        return self.title if self.title else self.content[:80]
