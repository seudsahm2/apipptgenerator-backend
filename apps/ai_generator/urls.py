from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_presentation, name='generate_presentation'),
    path('slide/<uuid:slide_id>/regenerate-image/', views.regenerate_slide_image, name='regenerate_slide_image'),
    path('status/', views.ai_status, name='ai_status'),
]
