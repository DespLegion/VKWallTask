from django.core.exceptions import ValidationError
from django.db import models


vk_api_versions = (
    ("5.154", "v5.154"),
    ("5.150", "v5.150"),
    ("5.140", "v5.140"),
    ("5.139", "v5.139"),
    ("5.131", "v5.131"),
    ("5.130", "v5.130"),
    ("5.126", "v5.126"),
    ("5.125", "v5.125"),
)


class VKBotConfigModel(models.Model):

    vk_api_key = models.TextField(
        null=False,
        blank=False,
        verbose_name="VK Bot API key",
        help_text="Group Bot API key (vk.com/{your_group_id}?act=tokens)"
    )
    vk_group_id = models.CharField(
        null=False,
        blank=False,
        verbose_name="VK Group ID",
        help_text="ID of group that bot part of"
    )

    vk_api_v = models.CharField(
        null=False,
        blank=False,
        max_length=6,
        choices=vk_api_versions,
        default="5.131",
        help_text="v5.131 is strongly recommended",
        verbose_name="VK API version"
    )

    comment_interaction_phrase = models.CharField(
        null=False,
        blank=False,
        verbose_name="Interaction phrase",
        help_text="The phrase with which the testing begins"
    )

    interaction_post = models.IntegerField(
        null=False,
        blank=False,
        verbose_name="Interaction post ID",
        help_text="ID of a post on the wall under which the interaction takes place. "
                  "If the ID = 0, the interaction will take place under all the posts of the group wall",
        default=0
    )

    bot_add_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Bot add date",
        help_text="Date when Bot were configured. Autocomplete field"
    )

    def __str__(self):
        return f"https://vk.com/club{self.vk_group_id}"

    def save(self, *args, **kwargs):
        if not self.pk and VKBotConfigModel.objects.exists():
            raise ValidationError(
                "You can have only ONE configured Bot!. "
                "If you want to add new configuration, delete configuration that already exists"
            )
        return super(VKBotConfigModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Bot Config"
