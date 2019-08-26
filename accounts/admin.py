from django.contrib import admin
from accounts.models import UserProfile, Staff

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Staff)
