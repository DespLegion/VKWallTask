from django.db import models
from django.db.models import Q, F


class CoverImgsModel(models.Model):
    cover_name = models.CharField(null=False, verbose_name="Name of Cover")

    cover_img = models.ImageField(null=False, blank=False, upload_to=f"imgs/covers/")

    is_activ_cover = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name="Use this cover",
    )

    cover_add_date = models.DateTimeField(auto_now_add=True, verbose_name="Cover add date")

    def save(self, *args, **kwargs):
        if self.is_activ_cover:
            CoverImgsModel.objects.filter(~Q(pk=self.pk) & Q(is_activ_cover=True)).update(is_activ_cover=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cover_name

    class Meta:
        verbose_name = "Cover"
        verbose_name_plural = "Covers"

