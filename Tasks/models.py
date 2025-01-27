from django.db import models
from django.conf import settings

class Task(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='عنوان',
    )

    description = models.TextField(
        verbose_name='توضیحات',
    )

    due_date = models.DateField(
        verbose_name='تاریخ سررسید'
    )

    completed = models.BooleanField(
        default=False,
        verbose_name='تکمیل شده/نشده',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ تعریف تسک'
    )

    updated_at = models.DateTimeField(
        verbose_name='تاریخ ویرایش تسک',
        null=True,
        blank=True,
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='ایجاد کننده'
    )

    def __str__(self):
        return self.title
