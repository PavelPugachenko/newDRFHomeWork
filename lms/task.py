from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from lms.models import Subscription


@shared_task
def mail_update_course_info(course_id):
    """Отправка сообщения об обновлении курса по подписке"""
    subscription_course = Subscription.objects.filter(course=course_id)
    subscription_course = subscription_course.select_related('user')

    print(f"Найдено {len(subscription_course)} подписок на курс {course_id}")
    for subscription in subscription_course:
        print(f"Отправка электронного письма на {subscription.user.email}")
        send_mail(
            subject="Обновление материалов курса",
            message=f'Курс {subscription.course.title} был обновлен.',
            from_email=EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=False
        )



