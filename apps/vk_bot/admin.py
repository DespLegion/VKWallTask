from django.contrib import admin
from .models import VKBotConfigModel


@admin.register(VKBotConfigModel)
class VKBotConfigsAdmin(admin.ModelAdmin):
    fields = [
        "vk_group_id",
        "vk_api_key",
        "interaction_post",
        "comment_interaction_phrase",
        "vk_api_v",
        "bot_add_date",
    ]
    readonly_fields = [
        "bot_add_date",
    ]
    list_display = [
        "vk_group_id",
        "vk_api_v",
    ]
