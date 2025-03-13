import urllib.parse
import zipfile
from io import BytesIO
from django.http import HttpResponse
from keydev_reports.report_tools import WordEditor
from .models import Intern


def generate_documents(request, intern):
    # Убедитесь, что fullname не пустое
    if not intern.fullname:
        intern.fullname = 'Без_имени'  # Название по умолчанию, если fullname пустое
    # Преобразуем fullname в безопасное имя файла
    safe_fullname = intern.fullname.replace(' ', '_')
    statement_path = "templates/Заявление на стажировку.docx"
    nda_path = "templates/NDA.docx"

    # Создаем экземпляр редактора для заявлени
    statement_editor = WordEditor(file_name=statement_path)
    statement_editor.docx_replace(
        fullname=intern.fullname,
        address=intern.address,
        id=intern.id,
        position=intern.position,
        email=intern.email,
        contact_info=intern.contact_info,
        start_date=intern.start_date,
        end_date=intern.end_date,
        application_date=intern.application_date,
    )
    # Создаем экземпляр редактора для nda
    nda_editor = WordEditor(file_name=nda_path)
    nda_editor.docx_replace(
        fullname=intern.fullname,
        id=intern.id,
        inn=intern.inn,
        passport=intern.passport,
        given_organ=intern.given_organ,
        address=intern.address,
        contact_info=intern.contact_info,
        application_date=intern.application_date,
    )

    # Создание zip-архива в памяти
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Генерация документа заявления
        statement_buffer = BytesIO()
        statement_editor.save(statement_buffer)
        statement_buffer.seek(0)
        zip_file.writestr(f'Заявление_{safe_fullname}.docx', statement_buffer.read())

        # Генерация документа NDA
        nda_buffer = BytesIO()
        nda_editor.save(nda_buffer)
        nda_buffer.seek(0)
        zip_file.writestr(f'NDA_{safe_fullname}.docx', nda_buffer.read())

    # Перемещаем указатель на начало архива
    zip_buffer.seek(0)

    # Кодируем имя файла для URL и задаем правильный Content-Disposition
    zip_filename = f'Документы_{safe_fullname}.zip'
    encoded_zip_filename = urllib.parse.quote(zip_filename)

    # Отправляем архив пользователю
    response = HttpResponse(zip_buffer.read(),
                            content_type="application/zip")
    response['Content-Disposition'] = f'attachment; filename="{encoded_zip_filename}"'
    return response
