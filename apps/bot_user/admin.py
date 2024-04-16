from django.contrib import admin
from .models import BotUser


@admin.register(BotUser)
class CustomUserAdmin(admin.ModelAdmin):
    fields = ["user_id", "user_firstname", "user_lastname", "user_q_status", "user_q_state", "user_add_date"]
    readonly_fields = (
        "user_firstname",
        "user_lastname",
        "user_id",
        "user_add_date",
    )
    list_display = (
        "user_firstname",
        "user_id",
        "user_q_status",
        "user_q_state",
        "user_add_date",
    )
    list_filter = (
        "user_id",
        "user_add_date"
    )
    search_fields = (
        "user_id",
        "user_firstname",
        "user_lastname"
    )
