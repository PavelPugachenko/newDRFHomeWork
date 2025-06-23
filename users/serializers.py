from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    payment_history = PaymentSerializer(many=True, read_only=True, source="payment_set")

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "payment_history",
        )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token["username"] = user.username
        token["email"] = user.email

        return token
