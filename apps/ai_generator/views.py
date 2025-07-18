from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.presentations.models import Presentation, Slide
from apps.presentations.serializers import PresentationSerializer
from .services import openai_service
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_presentation(request):
    """Generate a new presentation using AI"""
    try:
        # Get request data
        topic = request.data.get('topic', '').strip()
        slide_count = request.data.get('slideCount', 5)
        
        # Validation
        if not topic:
            return Response({
                'error': 'Topic is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(slide_count, int) or slide_count < 3 or slide_count > 10:
            return Response({
                'error': 'Slide count must be between 3 and 10'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check user credits
        user = request.user
        if user.ai_credits < 1:
            return Response({
                'error': 'Insufficient AI credits'
            }, status=status.HTTP_402_PAYMENT_REQUIRED)
        
        # Create presentation record
        presentation = Presentation.objects.create(
            user=user,
            title=f"Presentation about {topic}",
            topic=topic,
            slide_count=slide_count,
            status='generating'
        )
        
        try:
            # Generate content using OpenAI
            ai_content = openai_service.generate_presentation_content(topic, slide_count)
            
            # Update presentation with generated title and description
            presentation.title = ai_content.get('title', presentation.title)
            presentation.description = ai_content.get('description', '')
            presentation.status = 'completed'
            presentation.save()
            
            # Create slides
            slides_data = ai_content.get('slides', [])
            for slide_data in slides_data:
                # Generate image for slide (optional, can be done async)
                image_url = None
                image_prompt = slide_data.get('image_prompt', '')
                
                if image_prompt:
                    try:
                        image_url = openai_service.generate_slide_image(image_prompt)
                    except Exception as img_error:
                        logger.warning(f"Failed to generate image for slide: {str(img_error)}")
                
                # Create slide
                Slide.objects.create(
                    presentation=presentation,
                    title=slide_data.get('title', ''),
                    content=slide_data.get('content', ''),
                    image_url=image_url,
                    image_prompt=image_prompt,
                    slide_number=slide_data.get('slide_number', 1)
                )
            
            # Deduct AI credit
            user.ai_credits -= 1
            user.save()
            
            # Return the generated presentation
            serializer = PresentationSerializer(presentation)
            return Response({
                'presentation': serializer.data,
                'message': 'Presentation generated successfully',
                'credits_remaining': user.ai_credits
            }, status=status.HTTP_201_CREATED)
            
        except Exception as ai_error:
            # Update presentation status to failed
            presentation.status = 'failed'
            presentation.save()
            
            logger.error(f"AI generation failed: {str(ai_error)}")
            return Response({
                'error': 'Failed to generate presentation content',
                'details': str(ai_error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Presentation generation error: {str(e)}")
        return Response({
            'error': 'An unexpected error occurred',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def regenerate_slide_image(request, slide_id):
    """Regenerate image for a specific slide"""
    try:
        slide = Slide.objects.get(
            id=slide_id, 
            presentation__user=request.user
        )
        
        if not slide.image_prompt:
            return Response({
                'error': 'No image prompt available for this slide'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate new image
        new_image_url = openai_service.generate_slide_image(slide.image_prompt)
        
        if new_image_url:
            slide.image_url = new_image_url
            slide.save()
            
            return Response({
                'image_url': new_image_url,
                'message': 'Image regenerated successfully'
            })
        else:
            return Response({
                'error': 'Failed to generate new image'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Slide.DoesNotExist:
        return Response({
            'error': 'Slide not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Image regeneration error: {str(e)}")
        return Response({
            'error': 'Failed to regenerate image'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ai_status(request):
    """Get AI service status and user credits"""
    return Response({
        'openai_configured': bool(openai_service.openai.api_key),
        'user_credits': request.user.ai_credits,
        'model': openai_service.model,
        'image_model': openai_service.image_model
    })
