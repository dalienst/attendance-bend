from django.contrib import admin
from django.contrib.auth import get_user_model
from users.models import Profile, Units, RegisteredStudents, Approved

User = get_user_model()

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Units)
admin.site.register(RegisteredStudents)
admin.site.register(Approved)
