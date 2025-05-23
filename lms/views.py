from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from drf_yasg.openapi import Response
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscription
from lms.paginators import CustomPagination
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from lms.task import mail_update_course_info
from users.permissions import IsOwnerOrModerator


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_update(self, serializer):
        super().perform_update(serializer)
        course_id = serializer.instance.id
        mail_update_course_info.delay(course_id)

    @login_required
    def course_detail(request, course_id):
        course = get_object_or_404(Course, id=course_id)
        is_subscribed = course.is_subscribed(request.user)

        context = {
            'course': course,
            'is_subscribed': is_subscribed
        }

        return render(request, 'course_detail.html', context)

    @login_required
    def subscribe(request, course_id):
        course = get_object_or_404(Course, id=course_id)
        course.subscribe(request.user)
        return redirect('course_detail', course_id=course_id)

    @login_required
    def unsubscribe(request, course_id):
        course = get_object_or_404(Course, id=course_id)
        course.unsubscribe(request.user)
        return redirect('course_detail', course_id=course_id)


class LessonCreateApiView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]

class LessonListApiView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

class LessonRetrieveApiView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrModerator]

class LessonUpdateApiView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrModerator]

class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrModerator]

class SubscriptionCreateAPIView(CreateAPIView):
    """Эндпоинт создания подписки"""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        course_id = request.data.get('course')
        course = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course)
        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course, sign_up=True)
            message = 'Подписка добавлена'
        return Response({'message': message})


class SubscriptionListAPIView(ListAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()