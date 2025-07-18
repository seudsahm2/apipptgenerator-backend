from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apps.presentations.models import Presentation, Slide
from apps.presentations.serializers import PresentationSerializer
from .services import gemini_service
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_presentation(request):
    """Generate a new presentation using Google Gemini AI (FREE)"""
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
            # Generate content using Google Gemini (FREE)
            ai_content = gemini_service.generate_presentation_content(topic, slide_count)
            
            # Update presentation with generated title and description
            presentation.title = ai_content.get('title', presentation.title)
            presentation.description = ai_content.get('description', '')
            presentation.status = 'completed'
            presentation.save()
            
            # Create slides
            slides_data = ai_content.get('slides', [])
            for slide_data in slides_data:
                # Generate enhanced image prompt using Gemini
                image_prompt = slide_data.get('image_prompt', '')
                
                if not image_prompt:
                    try:
                        image_prompt = gemini_service.generate_slide_image_prompt(
                            slide_data.get('title', ''),
                            slide_data.get('content', '')
                        )
                    except Exception as img_error:
                        logger.warning(f"Failed to generate image prompt: {str(img_error)}")
                        image_prompt = f"Professional illustration for {slide_data.get('title', 'slide')}"
                
                # Create slide (no direct image generation with Gemini, just prompts)
                Slide.objects.create(
                    presentation=presentation,
                    title=slide_data.get('title', ''),
                    content=slide_data.get('content', ''),
                    image_url=None,  # No direct image generation
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
                'message': 'Presentation generated successfully using Google Gemini AI (Free)',
                'ai_provider': 'Google Gemini (Free)',
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
def regenerate_slide_content(request, slide_id):
    """Regenerate content for a specific slide using Gemini"""
    try:
        slide = Slide.objects.get(
            id=slide_id, 
            presentation__user=request.user
        )
        
        # Generate new content for the slide
        topic = slide.presentation.topic
        slide_title = slide.title
        
        prompt = f"""
        Regenerate content for a presentation slide about "{topic}".
        Current slide title: "{slide_title}"
        
        Generate 3 bullet points (maximum 12 words each) that are:
        - Professional and engaging
        - Relevant to the topic and title
        - Different from the current content
        
        Return only the bullet points in this format:
        • Point 1
        • Point 2  
        • Point 3
        """
        
        try:
            response = gemini_service.model.generate_content(prompt)
            new_content = response.text.strip() if response.text else slide.content
            
            # Update slide content
            slide.content = new_content
            slide.save()
            
            return Response({
                'content': new_content,
                'message': 'Slide content regenerated successfully'
            })
            
        except Exception as gen_error:
            logger.error(f"Content regeneration failed: {str(gen_error)}")
            return Response({
                'error': 'Failed to regenerate content'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Slide.DoesNotExist:
        return Response({
            'error': 'Slide not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Slide regeneration error: {str(e)}")
        return Response({
            'error': 'Failed to regenerate slide content'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enhance_presentation(request):
    """Enhance an existing presentation using Gemini"""
    try:
        presentation_id = request.data.get('presentation_id')
        if not presentation_id:
            return Response({
                'error': 'presentation_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        presentation = Presentation.objects.get(
            id=presentation_id,
            user=request.user
        )
        
        # Prepare current presentation data
        slides_data = []
        for slide in presentation.slides.all().order_by('slide_number'):
            slides_data.append({
                'slide_number': slide.slide_number,
                'title': slide.title,
                'content': slide.content,
                'image_prompt': slide.image_prompt
            })
        
        current_data = {
            'title': presentation.title,
            'description': presentation.description,
            'slides': slides_data
        }
        
        # Enhance using Gemini
        enhanced_data = gemini_service.enhance_presentation_content(current_data)
        
        # Update presentation
        presentation.title = enhanced_data.get('title', presentation.title)
        presentation.description = enhanced_data.get('description', presentation.description)
        presentation.save()
        
        # Update slides
        enhanced_slides = enhanced_data.get('slides', [])
        for enhanced_slide in enhanced_slides:
            try:
                slide = presentation.slides.get(slide_number=enhanced_slide.get('slide_number'))
                slide.title = enhanced_slide.get('title', slide.title)
                slide.content = enhanced_slide.get('content', slide.content)
                slide.image_prompt = enhanced_slide.get('image_prompt', slide.image_prompt)
                slide.save()
            except Slide.DoesNotExist:
                continue
        
        serializer = PresentationSerializer(presentation)
        return Response({
            'presentation': serializer.data,
            'message': 'Presentation enhanced successfully'
        })
        
    except Presentation.DoesNotExist:
        return Response({
            'error': 'Presentation not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Enhancement error: {str(e)}")
        return Response({
            'error': 'Failed to enhance presentation'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ai_status(request):
    """Get AI service status and user credits"""
    return Response({
        'ai_provider': 'Google Gemini',
        'is_free': True,
        'gemini_configured': bool(gemini_service.model),
        'user_credits': request.user.ai_credits,
        'model': gemini_service.model_name,
        'max_tokens': gemini_service.max_tokens,
        'rate_limit': '15 requests per minute (free tier)'
    })
