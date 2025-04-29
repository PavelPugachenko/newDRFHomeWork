from django_filters import rest_framework as filters
from users.models import Payment, Course, Lesson

class PaymentFilter(filters.FilterSet):
    course_id = filters.NumberFilter(field_name='paid_course__id')
    lesson_id = filters.NumberFilter(field_name='paid_lesson__id')
    payment_type = filters.ChoiceFilter(field_name='type', choices=Payment.PAYMENT_CHOICES)
    payment_date_gte = filters.DateFilter(field_name='payment_date', lookup_expr='gte')
    payment_date_lte = filters.DateFilter(field_name='payment_date', lookup_expr='lte')

    class Meta:
        model = Payment
        fields = ['course_id', 'lesson_id', 'payment_type', 'payment_date_gte', 'payment_date_lte']
