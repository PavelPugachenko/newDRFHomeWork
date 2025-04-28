from .views import MyTokenObtainPairView
from django.urls import path
from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserCreateAPIView, UserUpdateAPIView, UserListAPIView, PaymentCreateAPIView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

app_name = UsersConfig.name

urlpatterns = [
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path("register/", UserCreateAPIView.as_view(), name="register "),
    path("user/", UserListAPIView.as_view(), name="user_list"),
    path("user/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
    path('login/', TokenObtainPairView.as_view(), name='login/'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]



urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
