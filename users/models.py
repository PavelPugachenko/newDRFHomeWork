from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.core.validators import RegexValidator

from lms.models import Course, Lesson


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text="Обязательное поле. Максимум 150 символов."
    )
    email = models.EmailField(unique=True, max_length=254)
    phone = models.CharField(
        max_length=15,
        unique=True
    )
    city = models.CharField(max_length=100)
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        default='avatars/default.png'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.pk})


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ("BANK_TRANSFER", "Банковский перевод"),
        ("CASH", "Наличными"),
    ]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payment_date = models.DateField(default=datetime.now, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный курс",
        blank=True,
        null=True,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный урок",
        blank=True,
        null=True,
    )
    amount = models.DecimalField(decimal_places=2, max_digits=20, verbose_name="Сумма")
    type = models.CharField(
        max_length=50, choices=PAYMENT_CHOICES, verbose_name="Способ оплаты"
    )

    def __str__(self):
        return f"{self.owner} - {self.get_type_display()} - {self.amount}"