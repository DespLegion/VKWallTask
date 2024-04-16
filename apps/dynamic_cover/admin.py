from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import CoverImgsModel


@admin.register(CoverImgsModel)
class CoverImgsModelAdmin(admin.ModelAdmin):

    def get_img(self, obj):
        return mark_safe(f"<img src={obj.cover_img.url} width='140' height='70'")

    get_img.short_description = "Cover image preview"

    fields = ["cover_name", "cover_img", "get_img", "is_activ_cover", "cover_add_date",]
    readonly_fields = (
        "get_img",
        "cover_add_date",
    )
    list_display = (
        "cover_name",
        "get_img",
        "is_activ_cover",
        "cover_add_date",
    )
    list_filter = (
        "cover_name",
        "is_activ_cover",
        "cover_add_date",
    )
    search_fields = (
        "cover_name",
        "is_activ_cover",
        "cover_add_date",
    )
