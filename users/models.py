from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.core.validators import RegexValidator

class User(AbstractUser):
    username = None  # Отключаем поле username
    email = models.EmailField(unique=True, max_length=254)
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1-9\d{9,14}$',
                message="Номер телефона должен быть в международном формате, например: +79991234567"
            )
        ],
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
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.pk})

    def clean(self):
        super().clean()
        if not self.phone.startswith('+'):
            raise ValidationError({'phone': 'Номер телефона должен начинаться с +'})

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'