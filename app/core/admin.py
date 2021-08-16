from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User

# from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "is_staff", "is_active", "is_verified")
    list_filter = ("is_staff", "email")
    list_editable = ("is_verified", "is_active")
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Personal info", {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_verified",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates", {"classes": ("collapse",), "fields": ("created_at", "updated_at")}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    search_fields = ("email",)
    ordering = ("email",)

    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)
