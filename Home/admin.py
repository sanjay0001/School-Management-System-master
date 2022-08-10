from django.contrib import admin
from .models import Student, Teacher

# Register your models here.

#Registering Student model and Teacher model to the admin panel
admin.site.register(Student)
admin.site.register(Teacher)