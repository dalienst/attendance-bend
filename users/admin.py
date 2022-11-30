from django.contrib import admin
from django.contrib.auth import get_user_model
from users.models import (
    Profile,
    Units,
    RegisteredStudents,
    MarkStudents,
    RegisterUnits,
)

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "username",
        "email",
        "name",
    ]
    list_filter = [
        "name",
    ]


admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "bio",
        "location",
        "contact",
    ]
    list_filter = [
        "user",
    ]


admin.site.register(Profile, ProfileAdmin)


class UnitsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "code",
        "name",
        "lecturer",
    ]
    list_filter = [
        "lecturer",
        "code",
    ]


admin.site.register(Units, UnitsAdmin)


class RegisteredStudentsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "regnumber",
        "sname",
    ]
    list_filter = [
        "sname",
    ]


admin.site.register(RegisteredStudents, RegisteredStudentsAdmin)


class RegisterUnitsAdmin(admin.ModelAdmin):
    list_display = [
        "unit",
        "student",
    ]
    list_filter = [
        "unit",
    ]


admin.site.register(RegisterUnits, RegisterUnitsAdmin)


class MarkStudentsAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "unit",
        "status",
        "total",
    ]
    list_filter = [
        "unit",
        "student",
    ]


admin.site.register(MarkStudents, MarkStudentsAdmin)
