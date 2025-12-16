from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "phone",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("is_active", "is_staff")
    search_fields = ("username", "email", "phone")
    ordering = ("-id",)

    fieldsets = (
        ("Informations", {
            "fields": ("username", "email", "phone", "password")
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Dates", {
            "fields": ("last_login", "date_joined")
        }),
    )

    readonly_fields = ("last_login", "date_joined")
