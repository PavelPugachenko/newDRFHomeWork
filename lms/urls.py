from django.urls import path
from .views import (
    LessonCreateView,
    LessonDeleteView,
    LessonListView,
    LessonRetrieveView,
    LessonUpdateView,
    SubscriptionCreateView,
    SubscriptionListView,
)

app_name = "lms"

urlpatterns = [
    path('lesson/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson_delete'),
    path('lesson/list/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveView.as_view(), name='lesson_retrieve'),
    path('lesson/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson_update'),

    path('subscribe/', SubscriptionCreateView.as_view(), name='subscribe'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscription_list'),
]