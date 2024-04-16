from django.core.exceptions import ValidationError
from django.db import models


class QuestionsModel(models.Model):
    full_question = models.TextField(null=False, blank=False, verbose_name="Question")
    question_answer = models.TextField(null=False, blank=False, verbose_name="Question answer")

    question_add_date = models.DateTimeField(auto_now_add=True, verbose_name="Question add date")

    def __str__(self):
        return self.full_question

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class TestingsModel(models.Model):
    user = models.ForeignKey(
        "bot_user.BotUser",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="User"
    )

    testing_json = models.JSONField(null=False, blank=False, verbose_name="User generated testing")

    testing_user_answers = models.JSONField(null=True, blank=True, verbose_name="User answers")

    testing_status = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name="Testing successful completed?"
    )

    testing_res = models.IntegerField(null=True, blank=True, verbose_name="Testing score")

    testing_add_date = models.DateTimeField(auto_now_add=True, verbose_name="Question add date")

    def __str__(self):
        return f"{self.user.user_firstname} - {self.user.user_id}"

    class Meta:
        verbose_name = "Testing"
        verbose_name_plural = "Testings"


class TestingsConfig(models.Model):
    question_count = models.IntegerField(
        null=False,
        blank=False,
        verbose_name="Question count",
        default=5,
        help_text="The number of questions the user must answer to complete the testing"
    )

    def __str__(self):
        return str(self.question_count)

    def save(self, *args, **kwargs):
        if not self.pk and TestingsConfig.objects.exists():
            raise ValidationError(
                "You can have only ONE configured Testing!. "
                "If you want to add new Testing configuration, delete configuration that already exists"
            )
        return super(TestingsConfig, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Testings Config"
