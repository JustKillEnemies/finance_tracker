from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Operation(models.Model):
    class TypeOfMethod(models.IntegerChoices):
        CARD = 0, "Банковская карта"
        CASH = 1, "Наличные"
        QR = 2, "QR-код"
        SBP = 3, "СБП перевод"

    class TransactionType(models.IntegerChoices):
        EXPENSE = 0, "Расход"
        INCOME = 1, "Доход"

    name = models.CharField(max_length=255, verbose_name='Название операции')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    amount = models.FloatField(blank=False, verbose_name='Сумма')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, verbose_name='Категория', related_name="operations")
    method = models.PositiveSmallIntegerField(choices=TypeOfMethod.choices, default=TypeOfMethod.CARD, verbose_name='Метод оплаты')
    type = models.PositiveSmallIntegerField(choices=TransactionType.choices, default=TransactionType.EXPENSE, verbose_name='Тип операции')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')


# модель категорий
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Слаг')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь',)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('home')


class ContextMenu(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    url_name = models.CharField(max_length=100, verbose_name="Url")

    def __str__(self):
        return self.title

