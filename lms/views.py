from django.views.generic import TemplateView
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwnerOrModerator


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]


class LessonCreateApiView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsOwnerOrModerator]

class LessonListApiView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


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