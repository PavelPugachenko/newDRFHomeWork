from rest_framework import serializers
from users.models import Payment, User
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(ModelSerializer):
    payment_history = PaymentSerializer(many=True, read_only=True, source='payment_set')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'payment_history',)


