from django.db import models

from users.models import User


class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(
        max_length=200, verbose_name="full_name", help_text="Введите ваше Ф.И.О."
    )
    comment = models.TextField(
        verbose_name='comment', help_text='Введите комментарий', blank=True, null=True
    )
    owner = models.ForeignKey(User, verbose_name='owner', on_delete=models.SET_NULL, blank=True, null=True)


    class Meta:
        verbose_name='Клиент'
        verbose_name_plural='Клиенты'

    def __str__(self):
        return self.email

class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='subject', help_text='Введите тему письма')
    body = models.TextField(verbose_name='body', help_text='Введите текст письма')
    owner = models.ForeignKey(User, verbose_name='owner', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name='Сообщение'
        verbose_name_plural='Сообщения'

    def __str__(self):
        return self.subject

class Mailing(models.Model):
    start_date = models.DateTimeField(verbose_name='start_date', help_text='дата и время первой отправки рассылки',
                                      blank=True, null=True)
    period = models.CharField(max_length=10, verbose_name='period', choices=[
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ])
    status = models.CharField(max_length=10, verbose_name='status', choices=[
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
    ])

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='message')
    clients = models.ManyToManyField(Client, verbose_name='client', blank=True)
    owner = models.ForeignKey(User, verbose_name='owner', on_delete=models.SET_NULL, blank=True, null=True)
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

        permissions = [
            ('deactivate_mailing', 'Can deactivate mailing'),
            ('view_all_mailings', 'Can view all mailings'),
        ]

    def __str__(self):
        return f'Рассылка {self.id}'


class Attempt(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='mailing')
    date = models.DateTimeField(auto_now_add=True, verbose_name='date')
    status = models.CharField(max_length=10, verbose_name='status', choices=[
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ])
    response = models.TextField(blank=True, null=True, verbose_name='response')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'

    def __str__(self):
        return self.status



