"""
SlideCraft AI Backend URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# API Router
router = DefaultRouter()

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Routes
    path('api/auth/', include('apps.authentication.urls')),
    path('api/presentations/', include('apps.presentations.urls')),
    path('api/generate/', include('apps.ai_generator.urls')),
    path('api/export/', include('apps.exports.urls')),
    path('api/', include(router.urls)),
    
    # Health Check
    path('health/', include('apps.core.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin customization
admin.site.site_header = "SlideCraft AI Admin"
admin.site.site_title = "SlideCraft AI"
admin.site.index_title = "Welcome to SlideCraft AI Administration"
