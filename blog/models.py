from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='title', help_text='Введите заголовок блога')
    body = models.TextField(verbose_name='body', help_text='Введите текст блога')

    image = models.ImageField(
        upload_to="image/pictures",
        blank=True,
        null=True,
        verbose_name="image",
        help_text="Загрузите аватар блога",
    )
    publish_at = models.DateField(
        verbose_name="created_at", blank=True, null=True
    )

    view_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        default=0
    )

    class Meta:
        verbose_name = "блог"
        verbose_name_plural = "блоги"
        ordering = ['title']

    def __str__(self):
        return self.title