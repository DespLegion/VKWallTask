from django.contrib import admin
from .models import QuestionsModel, TestingsConfig, TestingsModel


@admin.register(QuestionsModel)
class QuestionsAdmin(admin.ModelAdmin):
    fields = ["full_question", "question_answer", "question_add_date",]
    readonly_fields = (
        "question_add_date",
    )
    list_display = (
        "full_question",
        "question_answer",
        "question_add_date",
    )
    list_filter = (
        "question_add_date",
    )
    search_fields = (
        "full_question",
        "question_answer",
        "question_add_date",
    )


@admin.register(TestingsConfig)
class TestingsConfigAdmin(admin.ModelAdmin):
    fields = ["question_count",]

    list_display = (
        "question_count",
    )


@admin.register(TestingsModel)
class TestingsConfigAdmin(admin.ModelAdmin):
    fields = ["id", "user", "testing_status", "testing_res", "testing_user_answers", "testing_json", "testing_add_date",]
    readonly_fields = (
        "id",
        "testing_user_answers",
        "testing_json",
        "testing_add_date",
        "testing_res",
    )
    list_display = (
        "id",
        "user",
        "testing_status",
        "testing_res",
        "testing_add_date",
    )
    list_filter = (
        "id",
        "user",
        "testing_res",
    )
    search_fields = (
        "user",
        "testing_add_date",
        "question_add_date",
        "testing_res",
        "testing_status",
    )
