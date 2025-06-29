from amqp import NotFound
from requests import Response
from rest_framework import generics, permissions, status
from .models import Lesson, Subscription, Course
from .serializers import LessonSerializer, SubscriptionSerializer


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()  # <-- добавьте это


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDeleteView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class SubscriptionCreateView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        course_id = self.request.data.get('course')
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Курс не найден"}, status=status.HTTP_404_NOT_FOUND)


class SubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()