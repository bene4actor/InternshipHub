from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Intern
from .utils import generate_nda





def download_nda_document(request, intern_id, report_id):
    # Получаем объект Intern
    # intern = get_object_or_404(Intern, id=intern_id)

    # Генерация документа
    response = generate_nda(pk=intern_id, report_id=report_id)
    return response
