from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'phone_no', 'country')
    list_filter = ('country',)
    search_fields = ('user__username',)