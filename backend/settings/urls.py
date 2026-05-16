from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Все наши модули подключаем под единый префикс api/v1/
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/projects/', include('apps.projects.urls')),
    path('api/v1/agile/', include('apps.agile.urls')),
]