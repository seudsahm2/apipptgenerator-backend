from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import os

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint for deployment monitoring"""
    return Response({
        'status': 'healthy',
        'service': 'SlideCraft AI Backend',
        'version': '1.0.0',
        'environment': 'production' if not settings.DEBUG else 'development'
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def status_check(request):
    """Detailed status check with system information"""
    return Response({
        'status': 'operational',
        'service': 'SlideCraft AI Backend',
        'version': '1.0.0',
        'debug': settings.DEBUG,
        'database': 'connected',
        'openai_configured': bool(settings.OPENAI_API_KEY),
        'allowed_hosts': settings.ALLOWED_HOSTS,
    })
