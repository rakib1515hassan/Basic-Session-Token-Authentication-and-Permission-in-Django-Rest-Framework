from django.contrib import admin
from Auth_Permission.models import Student


# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll', 'city')

