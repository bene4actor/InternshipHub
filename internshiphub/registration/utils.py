import os
import uuid
from urllib.parse import unquote,quote
from django.shortcuts import get_object_or_404
from io import BytesIO
from django.http import HttpResponse
from django.utils.text import slugify
from pydantic import ValidationError
from .proxy_models import InternProxy, Intern
from internshiphub.keydev_reports.report_tools import WordEditor
from internshiphub.keydev_reports.models import ReportTemplate




def generate_nda(pk, report_id):
    # загружаем данные из прокси модели
    obj = InternProxy.proxy_objects.get_all_data().get(pk=pk)
    data = obj.get_report_data()
    report = get_object_or_404(ReportTemplate, pk=report_id)

    #Убедитесь, что fullname не пустое
    if data.get("full_name") is None:
        data["full_name"] = 'Без_имени'  # Название по умолчанию, если fullname пустое

    # Проверяем, подписано ли Заявление
    if not data.get("is_application_signed"):
        raise ValueError(f"{report.name} не может быть сгенерирован, так как Заявление не подписано.")

    # Преобразуем fullname в безопасное имя файла
    safe_fullname = slugify(data.get("full_name"))

    # Путь к шаблону
    template_path = report.file.path
    filename = report.filename()
    # Проверка существования шаблона
    if not os.path.exists(template_path):
        raise ValueError(f"Шаблон {template_path} не найден.")

    # Генерация NDA
    doc_editor = WordEditor(file_name=template_path)
    doc_editor.docx_replace(**data)

    # Сохраняем документ в BytesIO
    doc_buffer = BytesIO()
    doc_editor.save(doc_buffer)
    doc_buffer.seek(0)

    # Формируем имя файла
    filename = f'{filename}_{safe_fullname[:50]}.docx'
    encode_filename = quote(filename)

    # Создаем HttpResponse для возврата файла
    response = HttpResponse(
        doc_buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response["Content-Disposition"] = f'attachment; filename="{encode_filename}"'
    return response

# def generate_documents(intern):
#
#     # Генерация номера заявления, если его еще нет
#     if not intern.application_number:
#         intern.application_number = generate_application_number()
#         intern.save()
#
#     # Убедитесь, что fullname не пустое
#     if not intern.full_name:
#         intern.full_name = 'Без_имени'  # Название по умолчанию, если fullname пустое
#     # Преобразуем fullname в безопасное имя файла
#     safe_fullname = intern.full_name.replace(' ', '_')
#     template_path = "keydev_reports/report_templates/Заявление_на_стажировку.docx"
#
#     context = {
#         'full_name': intern.full_name,
#         'email': intern.email,
#         'contact_info': intern.contact_info,
#         'internship_start': intern.internship_start.strftime('%d.%m.%Y') if intern.internship_start else 'Не указано',
#         'internship_end': intern.internship_end.strftime('%d.%m.%Y') if intern.internship_end else 'Не указано',
#         'created_at': intern.created_at.strftime('%d.%m.%Y %H:%M') if intern.created_at else 'Не указано',
#         'position': intern.position,
#         'address': intern.address,
#         'app_number': intern.application_number,
#         'ID': intern.ID_doc,
#         'date_of_issue': intern.date_of_issue.strftime('%d.%m.%Y'),
#         'INN': intern.INN,
#         'authority': intern.authority,
#     }
#
#     # Создаем экземпляр редактора для документа
#     word_editor = WordEditor(file_name=template_path)
#     word_editor.docx_replace(**context)
#
#     # Генерация документа
#     with BytesIO() as docx_buffer:
#         word_editor.save(docx_buffer)
#         docx_buffer.seek(0)
#         # Отправляем файл пользователю для скачивания
#
#         filename = f'Заявление_{safe_fullname}.docx'
#         encode_filename = urllib.parse.quote(filename)
#         response = HttpResponse(
#             docx_buffer.getvalue(),
#             content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#         )
#         response["Content-Disposition"] = f'attachment; filename="{encode_filename}"'
#         return response
#
#
# def generate_nda(intern):
#     # Проверяем, подписано ли Заявление
#     if not intern.is_application_signed:
#         raise ValidationError("NDA не может быть сгенерирован, так как Заявление не подписано.")
#
#     # Преобразуем fullname в безопасное имя файла
#     safe_fullname = slugify(intern.full_name) if intern.full_name else 'Без_имени'
#
#     # Путь к шаблону NDA
#     nda_template_path = "keydev_reports/report_templates/NDA.docx"
#
#     # Проверка существования шаблона
#     if not os.path.exists(nda_template_path):
#         raise ValidationError(f"Шаблон {nda_template_path} не найден.")
#
#     # Данные для подстановки в шаблон
#     context = {
#         'full_name': intern.full_name,
#         'email': intern.email,
#         'contact_info': intern.contact_info,
#         'internship_start': intern.internship_start.strftime('%d.%m.%Y') if intern.internship_start else 'Не указано',
#         'internship_end': intern.internship_end.strftime('%d.%m.%Y') if intern.internship_end else 'Не указано',
#         'created_at': intern.created_at.strftime('%d.%m.%Y %H:%M') if intern.created_at else 'Не указано',
#         'updated_at': intern.updated_at.strftime('%d.%m.%Y %H:%M') if intern.updated_at else 'Не указано',
#         'position': intern.position,
#         'address': intern.address,
#         'app_number': intern.application_number,
#         'ID': intern.ID_doc,
#         'date_of_issue': intern.date_of_issue.strftime('%d.%m.%Y'),
#         'INN': intern.INN,
#         'authority': intern.authority,
#     }
#
#     # Генерация NDA
#     nda_editor = WordEditor(file_name=nda_template_path)
#     nda_editor.docx_replace(**context)
#
#     # Сохраняем документ в BytesIO
#     nda_buffer = BytesIO()
#     nda_editor.save(nda_buffer)
#     nda_buffer.seek(0)
#
#     # Формируем имя файла
#     nda_filename = f'NDA_{safe_fullname[:50]}.docx'
#     encode_filename = urllib.parse.quote(nda_filename)
#
#     # Создаем HttpResponse для возврата файла
#     response = HttpResponse(
#         nda_buffer.getvalue(),
#         content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#     )
#     response["Content-Disposition"] = f'attachment; filename="{nda_filename}"'
#     return response
