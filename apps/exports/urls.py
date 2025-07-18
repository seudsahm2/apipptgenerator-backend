from django.urls import path
from . import views

urlpatterns = [
    path('pptx/', views.export_pptx, name='export_pptx'),
    path('pdf/', views.export_pdf, name='export_pdf'),
    path('formats/', views.export_formats, name='export_formats'),
]
