from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import path, include
from django.conf.urls.static import static  
from rest_framework import routers, serializers, viewsets

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
