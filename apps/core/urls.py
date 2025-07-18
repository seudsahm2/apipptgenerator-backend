from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_check, name='health_check'),
    path('status/', views.status_check, name='status_check'),
]
