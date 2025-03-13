from django.db import models


class Intern(models.Model):
    fullname = models.CharField('ФИО', max_length=255, null=True, blank=True)
    email = models.EmailField("Почта", default=None, null=True)
    inn = models.CharField("ИНН", max_length=20, null=True, blank=True)
    passport = models.CharField("Паспортные данные", max_length=255, null=True, blank=True)
    given_organ = models.CharField("Орган выдачи", max_length=255, null=True, blank=True)
    address = models.CharField("Адрес", max_length=255, null=True, blank=True)
    position = models.CharField("Должность", max_length=255, null=True, blank=True)
    contact_info = models.TextField('Контактные данные', null=True, blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    start_date = models.DateField('Дата начала', null=True, blank=True)
    end_date = models.DateField('Дата окончания', null=True, blank=True)
    application_date = models.DateField('Дата подачи заявления', null=True, blank=True)

    class Meta:
        verbose_name = 'Стажёр'
        verbose_name_plural = 'Стажёры'

    def __str__(self):
        return self.fullname
