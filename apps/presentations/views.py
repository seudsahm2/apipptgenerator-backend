from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Presentation, Slide, PresentationTemplate
from .serializers import (
    PresentationSerializer,
    PresentationCreateSerializer,
    PresentationListSerializer,
    SlideSerializer,
    PresentationTemplateSerializer
)

class PresentationViewSet(viewsets.ModelViewSet):
    """Presentation CRUD operations"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Presentation.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PresentationCreateSerializer
        elif self.action == 'list':
            return PresentationListSerializer
        return PresentationSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def slides(self, request, pk=None):
        """Get slides for a presentation"""
        presentation = self.get_object()
        slides = presentation.slides.all()
        serializer = SlideSerializer(slides, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """Duplicate a presentation"""
        original = self.get_object()
        
        # Create new presentation
        new_presentation = Presentation.objects.create(
            user=request.user,
            title=f"{original.title} (Copy)",
            description=original.description,
            topic=original.topic,
            slide_count=original.slide_count
        )
        
        # Duplicate slides
        for slide in original.slides.all():
            Slide.objects.create(
                presentation=new_presentation,
                title=slide.title,
                content=slide.content,
                image_url=slide.image_url,
                image_prompt=slide.image_prompt,
                slide_number=slide.slide_number,
                background_color=slide.background_color,
                text_color=slide.text_color
            )
        
        serializer = PresentationSerializer(new_presentation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SlideViewSet(viewsets.ModelViewSet):
    """Slide CRUD operations"""
    serializer_class = SlideSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Slide.objects.filter(presentation__user=self.request.user)

class PresentationTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """Presentation template operations"""
    queryset = PresentationTemplate.objects.all()
    serializer_class = PresentationTemplateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset
