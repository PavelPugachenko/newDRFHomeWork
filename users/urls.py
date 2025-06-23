from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.apps import UsersConfig
from users.views import (PaymentCreateAPIView, PaymentListAPIView,
                         UserCreateAPIView, UserListAPIView, UserUpdateAPIView)

app_name = UsersConfig.name


urlpatterns = [
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path("register/", UserCreateAPIView.as_view(), name="register "),
    path("user/", UserListAPIView.as_view(), name="user_list"),
    path("user/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path("login/", TokenObtainPairView.as_view(), name="login/"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]
