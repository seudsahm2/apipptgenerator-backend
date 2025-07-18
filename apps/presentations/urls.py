from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.PresentationViewSet, basename='presentations')
router.register(r'slides', views.SlideViewSet, basename='slides')
router.register(r'templates', views.PresentationTemplateViewSet, basename='templates')

urlpatterns = [
    path('', include(router.urls)),
]
