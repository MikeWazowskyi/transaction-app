from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'email', 'account', 'tax_id_number'
    )


admin.site.register(CustomUser, CustomUserAdmin)
