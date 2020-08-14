from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core import models

class UserAdmin(BaseUserAdmin):
    """To be used in displaying the User model"""
    ordering = ['id']
    list_display = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        #('Personal info', {'fields': ('',)}),
        (
            'Permissions', 
            {   
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        ('Important dates', {'fields': ('last_login',)}),
    )

    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    ) 


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Profile)
admin.site.register(models.Message)
admin.site.register(models.FriendRequest)
admin.site.register(models.Post)