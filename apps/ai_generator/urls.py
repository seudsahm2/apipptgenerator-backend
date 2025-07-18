from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_presentation, name='generate_presentation'),
    path('slide/<uuid:slide_id>/regenerate/', views.regenerate_slide_content, name='regenerate_slide_content'),
    path('presentation/enhance/', views.enhance_presentation, name='enhance_presentation'),
    path('status/', views.ai_status, name='ai_status'),
]
