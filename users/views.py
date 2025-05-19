from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from lms.models import Course
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.filters import PaymentFilter
from rest_framework import viewsets

from users.services import create_stripe_product, create_stripe_price, create_stripe_session


# Регистрация пользователей (без авторизации)
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(serializer.validated_data['password'])
        user.save()

# Просмотр списка пользователей (с авторизацией)
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# Обновление пользователя (с авторизацией)
class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# Детальный просмотр пользователя (с авторизацией)
class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# Удаление пользователя (с авторизацией)
class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# Работа с платежами
class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_lesson', 'paid_course', 'payment_type',)
    ordering_fields = ('date',)
    permission_classes = [IsAuthenticated]

class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        course_id = self.request.data.get('course_id')
        course = Course.objects.all().get(id=course_id)
        course_title = course.title
        course_price = course.price
        stripe_product_id = create_stripe_product(course_title)
        stripe_price = create_stripe_price(stripe_product_id, course_price)
        session_id, payment_link = create_stripe_session(stripe_price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

# Авторизация
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
