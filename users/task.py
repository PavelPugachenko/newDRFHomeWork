from datetime import timedelta, timezone
from celery import shared_task
from dateutil.relativedelta import relativedelta

from users.models import User


@shared_task
def check_last_login():
    """Проверка последнего входа пользователей и отключение неактивных пользователей"""
    month_ago = timezone.now() - relativedelta(months=1)
    users = User.objects.filter(last_login__lt=month_ago, is_active=True)
    users.update(is_active=False)

    for user in users:
        if month_ago - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
            print(f'Пользователь {user.email} отключен')
        else:
            print(f'Пользователь {user.email} активен')
