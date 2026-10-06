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


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class CatalogItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=200, verbose_name="Название")
    short_description = models.TextField(verbose_name="Краткое описание")
    full_description = models.TextField(verbose_name="Полное описание")
    price = models.DecimalField(max_digits=10, decimal_places=1, verbose_name="Цена", blank=True, null=True)
    image = models.FileField(upload_to='catalog/', verbose_name="Картинка", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Элемент каталога"
        verbose_name_plural = "Элементы каталога"

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтверждён'),
        ('cancelled', 'Отменён'),
        ('completed', 'Выполнен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Итоговая стоимость")
    created_at = models.DateTimeField(default=datetime.now, verbose_name="Дата создания")

    def __str__(self):
        return f"Заказ №{self.id} от {self.user.username}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(CatalogItem, on_delete=models.CASCADE, verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена на момент заказа")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказа"