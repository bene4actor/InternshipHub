from django.db import models
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.urls import path, reverse
from django.utils.html import format_html
from django.http import HttpResponseRedirect

from .forms import InternAdminForm
from .models import Intern
from .utils import generate_documents
from django.contrib.admin import forms



class InternAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "contact_info", "end_date", "start_date", "download_documents_button")
    form = InternAdminForm
    fieldsets = (
        (None, {
            'fields': ('fullname', 'email', 'inn', 'birth_date', 'contact_info', 'start_date', 'end_date', 'passport',
                       'given_organ', 'address', 'position', 'application_date')
        }),
    )
    def download_documents_button(self, obj):
        # Генерируем правильный URL с помощью reverse
        url = reverse('admin:interns_intern_download', args=[obj.id])
        return format_html('<a class="button" href="{}">📄 Скачать документы</a>', url)

    download_documents_button.short_description = "Документы"
    download_documents_button.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:intern_id>/download/', self.admin_site.admin_view(self.download_documents), name='interns_intern_download'),
        ]
        return custom_urls + urls

    def download_documents(self, request, intern_id):
        intern = get_object_or_404(Intern, id=intern_id)
        return generate_documents(request, intern)

admin.site.register(Intern, InternAdmin)
