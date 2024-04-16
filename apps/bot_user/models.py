from django.db import models
from apps.testing.models import TestingsConfig


user_q_statuses = (
    ("0", "not started"),
    ("1", "in progress"),
    ("2", "complete"),
)


def get_q_states():
    user_q_states = [
        ["0", "not started"],
    ]
    testings_config = TestingsConfig.objects.first()
    for question_number in range(0, testings_config.question_count):
        user_q_states.append(
            [f"{question_number+1}", f"On question {question_number+1}"],
        )
    user_q_states.append(
        ["done", "Testing complete"]
    )
    return user_q_states


class BotUser(models.Model):
    user_id = models.BigIntegerField(unique=True, null=False, verbose_name="User ID")
    user_firstname = models.CharField(null=False, verbose_name="Firstname")
    user_lastname = models.CharField(null=True, blank=True, verbose_name="Lastname")

    user_add_date = models.DateTimeField(auto_now_add=True, verbose_name="Registration date")

    user_q_status = models.CharField(
        null=False,
        blank=False,
        choices=user_q_statuses,
        default="not started",
        verbose_name="User testing status"
    )

    user_q_state = models.CharField(
        null=False,
        blank=False,
        choices=get_q_states(),
        default="not started",
        verbose_name="User question number (if testing started)"
    )

    def __str__(self):
        return f"{self.user_firstname} - {self.user_id}"

    class Meta:
        verbose_name = "Bot User"
        verbose_name_plural = "Bot Users"
