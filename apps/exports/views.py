from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from apps.presentations.models import Presentation
from .services import pptx_service, pdf_service
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def export_pptx(request):
    """Export presentation to PPTX format"""
    try:
        presentation_id = request.data.get('presentation_id')
        if not presentation_id:
            return Response({
                'error': 'presentation_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get presentation
        presentation = get_object_or_404(
            Presentation, 
            id=presentation_id, 
            user=request.user
        )
        
        # Check if presentation has slides
        if not presentation.slides.exists():
            return Response({
                'error': 'Presentation has no slides to export'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate PPTX
        pptx_stream = pptx_service.create_pptx(presentation)
        
        # Create response
        response = HttpResponse(
            pptx_stream.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
        response['Content-Disposition'] = f'attachment; filename="{presentation.title}.pptx"'
        
        return response
        
    except Exception as e:
        logger.error(f"PPTX export error: {str(e)}")
        return Response({
            'error': 'Failed to export presentation',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def export_pdf(request):
    """Export presentation to PDF format"""
    try:
        presentation_id = request.data.get('presentation_id')
        if not presentation_id:
            return Response({
                'error': 'presentation_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get presentation
        presentation = get_object_or_404(
            Presentation, 
            id=presentation_id, 
            user=request.user
        )
        
        # Check if presentation has slides
        if not presentation.slides.exists():
            return Response({
                'error': 'Presentation has no slides to export'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate PDF
        pdf_stream = pdf_service.create_pdf(presentation)
        
        # Create response
        response = HttpResponse(
            pdf_stream.getvalue(),
            content_type='application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename="{presentation.title}.pdf"'
        
        return response
        
    except Exception as e:
        logger.error(f"PDF export error: {str(e)}")
        return Response({
            'error': 'Failed to export presentation',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_formats(request):
    """Get available export formats"""
    return Response({
        'formats': [
            {
                'name': 'PowerPoint',
                'extension': 'pptx',
                'mime_type': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
                'description': 'Microsoft PowerPoint format'
            },
            {
                'name': 'PDF',
                'extension': 'pdf',
                'mime_type': 'application/pdf',
                'description': 'Portable Document Format'
            }
        ]
    })
