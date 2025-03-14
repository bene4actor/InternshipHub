from django.core.exceptions import ValidationError
from django.db import models

from ..keydev_reports.models import ReportTemplate


# from .utils import generate_documents


class Intern(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    position = models.CharField(max_length=255, verbose_name="Название позиции")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    email = models.EmailField(verbose_name="Почта")
    contact_info = models.CharField(max_length=255, verbose_name="Контактные данные")
    internship_start = models.DateField(verbose_name="Начало стажировки")
    internship_end = models.DateField(verbose_name="Окончание стажировки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_application_signed = models.BooleanField(default=False, verbose_name="Заявление подписано")
    application_number = models.CharField(max_length=50, unique=True, blank=True, null=True,
                                          verbose_name="Номер заявления")
    ID_doc = models.CharField(max_length=20, verbose_name="Номер документа")
    INN = models.CharField("ИНН", max_length=20, null=True, blank=True)
    authority = models.CharField(max_length=255, verbose_name="Орган выдачи")
    date_of_issue = models.DateField(verbose_name="Дата выдачи")

    # Связь с шаблонами отчетов
    # reports = models.ManyToManyField(ReportTemplate, related_name='interns', verbose_name='Шаблоны отчетов')


    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Стажер'
        verbose_name_plural = 'Стажеры'

    # def save(self, *args, **kwargs):
    #     try:
    #         generate_documents(self)
    #     except Exception as e:
    #         raise ValidationError(f"Ошибка при генерации документов: {str(e)}")
    #     super().save(*args, **kwargs)
