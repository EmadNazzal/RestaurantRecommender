"""This file contains the admin configuration for the user_management app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user_management.models import Preference, Profile, TimeStamp, User, UserLikedRestaurant, UserPreference  # type: ignore


class CustomUserAdmin(UserAdmin):
    """Custom User admin class."""

    model = User
    list_display = ("id", "first_name", "surname", "email",
                    "is_active", "date_joined", "last_login")
    search_fields = ("email", "first_name", "surname")
    list_filter = ("is_active", "date_joined")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "surname")}),
        ("Permissions", {"fields": ("is_active", "is_staff",
         "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "surname",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )


class ProfileAdmin(admin.ModelAdmin):
    """Profile admin class."""

    list_display = ("id", "user", "first_name", "surname", "avatar")


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(TimeStamp)
admin.site.register(Preference)
admin.site.register(UserPreference)
admin.site.register(UserLikedRestaurant)
