from django.urls import path
from .views import html_download, csv_enviado, download_modelo

urlpatterns = [
    path('', csv_enviado, name='upload_csv'),
    # path('process-csv', ext_data, name='process'),
    path('download/', html_download, name='download_html'),
    path('modelo-csv/', download_modelo, name='download_csv'),
]