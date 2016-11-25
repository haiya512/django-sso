from django.contrib import admin

from models import LoginDetail


class LoginDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'login_count', 'login_from_url')
admin.site.register(LoginDetail, LoginDetailAdmin)
