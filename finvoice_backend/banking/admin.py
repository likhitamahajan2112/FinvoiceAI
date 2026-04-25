from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Transaction

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('account_number', 'balance', 'is_staff', 'is_superuser')
    search_fields = ('account_number',)
    ordering = ('account_number',)

    fieldsets = (
        (None, {'fields': ('account_number', 'password', 'pin', 'balance')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('account_number', 'pin', 'balance', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'type', 'description', 'date')
    search_fields = ('user__account_number', 'description')
    list_filter = ('type', 'date')