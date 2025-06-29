from django.urls import reverse
from requests import Response
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import NotFound

from users.models import User

from .models import Course, Lesson, Subscription


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="www@yandex.com")
        self.course = Course.objects.create(
            title="Основы Английского",
            description="научитесь грамотно говорить в любой стране",
        )
        self.lesson = Lesson.objects.create(
            title="жи-ши с буквой и", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        url = reverse("lms:lesson_create")
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "А теперь граматика",
            "description": "крутой урок, бесспорно",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_Youtube(self):
        url = reverse("lms:lesson_create")
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "А теперь граматика",
            "description": "крутой урок, бесспорно",
            "course": self.course.pk,
            "owner": self.user.pk,
            "video_url": "https://www.youtube.com/",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_create_lesson_no_Youtube(self):
        url = reverse("lms:lesson_create")
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "А теперь граматика",
            "description": "крутой урок, бесспорно",
            "course": self.course.pk,
            "owner": self.user.pk,
            "video_url": "https://www.youtube.ru/",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_create_lesson_YouTube(self):
        url = reverse("lms:lesson_create")
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "А теперь граматика",
            "description": "крутой урок, бесспорно",
            "course": self.course.pk,
            "owner": self.user.pk,
            "video_url": "https://www.youtube.com/YaEBglkCFVc",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)


    def test_lesson_retrieve(self):
        url = reverse("lms:lesson_retrieve", args=(self.lesson.pk,))
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update(self):
        url = reverse("lms:lesson_update", args=[self.lesson.id])
        data = {"title": "Граматика", "video_url": self.lesson.video_url}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Граматика")

    def test_lesson_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("lms:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("lms:lesson_list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(email="www@yandex.com")

        # Создаем курс
        self.course = Course.objects.create(
            title="Основы Английского",
            description="научитесь грамотно говорить в любой стране",
            owner=self.user  # если у вас есть поле owner в модели Course
        )

        # Создаем урок
        self.lesson = Lesson.objects.create(
            title="жи-ши с буквой и",
            course=self.course,
            owner=self.user
        )

        # Создаем подписку
        self.subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
            is_subscribe=True  # если это нужно для тестов
        )

        # Авторизуем пользователя для API-запросов
        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        # Авторизуем пользователя
        self.client.force_authenticate(user=self.user)

        url = reverse("lms:subscribe")
        data = {"course": self.course.id}  # убедитесь, что имя поля "course"

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscription_list(self):
        url = reverse("lms:subscription_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["course"], self.course.id)

    def test_subscribe_to_course_no_ex(self):
        url = reverse('lms:subscribe')
        data = {"course": 999999}  # несуществующий ID
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscribe_to_course_no_au(self):
        url = reverse("lms:subscribe")
        data = {"course": self.course.id}

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
