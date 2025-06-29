from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer

from .models import Course, Lesson, Subscription
from .validators import YoutubeValidators


class LessonSerializer(ModelSerializer):
    validators = [YoutubeValidators(field="video_url")]

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    count_of_lessons = serializers.SerializerMethodField()
    info_lessons = serializers.SerializerMethodField()

    def get_count_of_lessons(self, obj):
        return obj.lesson_set.count()

    def get_info_lessons(self, obj):
        lessons = obj.lesson_set.all()
        return LessonSerializer(lessons, many=True).data

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "preview",
            "count_of_lessons",
            "info_lessons",
        )


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"

    def test_subscribe_to_course(self):
        url = reverse('lms:subscribe')
        data = {'course': self.course.id}  # убедитесь, что поле называется так же, как в сериалайзере
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def validate(self, data):
        if not Course.objects.filter(id=data['course'].id).exists():
            raise serializers.ValidationError("Course does not exist.")
        return data