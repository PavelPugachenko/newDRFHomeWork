from django.contrib import admin

from .models import Course, Lesson, Payment, User

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Payment)
admin.site.register(User)
