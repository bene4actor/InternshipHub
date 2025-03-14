from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from internshiphub.keydev_reports.models import ReportTemplate
from .models import Intern
from urllib.parse import quote
import os


@admin.register(Intern)
class InternAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'position', 'download_link', )  # Добавляем кастомную колонку
    search_fields = ('full_name', 'email')
    exclude = ("created_at", "application_number")
    readonly_fields = ("created_at",)

    # def download_link(self, obj):
    #     # Генерация ссылки для скачивания документа
    #     url = reverse('download_intern_document', args=[obj.id])
    #     return format_html('<a href="{}">Скачать документ</a>', url)
    # download_link.short_description = 'Документ'  # Название колонки

    # def download_nda_link(self, obj):
    #     if obj.is_application_signed:
    #         url = reverse('download_nda', args=[obj.id])
    #         return format_html('<a href="{}">📄 Скачать NDA</a>', url)
    #     return "Заявление не подписано"
    # download_nda_link.short_description = 'NDA'


    def download_link(self, obj):
        """Generates a dropdown with all ReportTemplate files"""
        reports = ReportTemplate.objects.all()  # Fetch all reports

        if not reports.exists():
            return "No Reports Available"

        dropdown_html = '<select onchange="">'
        dropdown_html += '<option value="">download Report</option>'  # Default option

        for report in reports:
            url = reverse('download_nda', kwargs={"intern_id":obj.id,"report_id":report.id})
            dropdown_html += f'<option onClick="if(this.value) window.open(this.value, \'_self\');" value="{url}">{report.name}</option>'

        dropdown_html += '</select>'

        return format_html(dropdown_html)

    download_link.short_description = 'Reports'

