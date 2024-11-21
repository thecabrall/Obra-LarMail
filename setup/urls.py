from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('https://obra-larmail.onrender.com',include('produtos.urls'))
]
