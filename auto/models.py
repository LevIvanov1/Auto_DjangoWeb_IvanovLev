from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib import admin
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name="Опубликована")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Автор")
    image = models.FileField(default='temp.jpg', upload_to='', verbose_name="Путь к картинке")

    def get_absolute_url(self):
        return reverse('blogpost', args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-posted']
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"

class Comment(models.Model):
    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(default=datetime.now(), verbose_name="Дата добавления")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья")

    def __str__(self):
        return f"Комментарий {self.id} от {self.author}"

    class Meta:
        ordering = ['-date']
        verbose_name = "Комментарий к статье"
        verbose_name_plural = "Комментарии к статьям"

admin.site.register(Comment)
admin.site.register(Blog)

