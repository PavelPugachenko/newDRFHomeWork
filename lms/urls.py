from django.urls import path

from lms.apps import LmsConfig
from rest_framework.routers import DefaultRouter
from lms.views import CourseViewSet, HomePageView, LessonListApiView, LessonRetrieveApiView, LessonCreateApiView, \
    LessonDestroyApiView, LessonUpdateApiView

app_name = LmsConfig.name

router= DefaultRouter()


router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path("lessons/<int:pk>/delete/",LessonDestroyApiView.as_view(),name="lessons_delete"),
    path("lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"),
] +router.urls

