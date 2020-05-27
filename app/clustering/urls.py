from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import file_list

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('', views.file_list, name='file_list'),
    path('result/<int:number>', views.result, name='result'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)