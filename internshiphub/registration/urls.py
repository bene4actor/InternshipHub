from django.urls import path
from .views import download_nda_document

urlpatterns = [
    path('download_nda/<int:intern_id>/<str:report_id>/', download_nda_document, name='download_nda'),
]
