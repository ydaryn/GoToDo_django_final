from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Подключаем все эндпоинты из accounts (логин, регистр, профиль, рефреш)
    path('api/v1/', include('apps.accounts.urls')),
]