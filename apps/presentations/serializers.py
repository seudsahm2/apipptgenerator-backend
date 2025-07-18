from rest_framework import serializers
from .models import Presentation, Slide, PresentationTemplate

class SlideSerializer(serializers.ModelSerializer):
    """Slide serializer"""
    class Meta:
        model = Slide
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class PresentationSerializer(serializers.ModelSerializer):
    """Presentation serializer with slides"""
    slides = SlideSerializer(many=True, read_only=True)
    
    class Meta:
        model = Presentation
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

class PresentationCreateSerializer(serializers.ModelSerializer):
    """Presentation creation serializer"""
    class Meta:
        model = Presentation
        fields = ('title', 'description', 'topic', 'slide_count')
    
    def validate_slide_count(self, value):
        if value < 3 or value > 10:
            raise serializers.ValidationError("Slide count must be between 3 and 10")
        return value

class PresentationListSerializer(serializers.ModelSerializer):
    """Simplified presentation serializer for lists"""
    slide_count_actual = serializers.SerializerMethodField()
    
    class Meta:
        model = Presentation
        fields = ('id', 'title', 'description', 'status', 'thumbnail', 
                 'slide_count', 'slide_count_actual', 'created_at', 'updated_at')
    
    def get_slide_count_actual(self, obj):
        return obj.slides.count()

class PresentationTemplateSerializer(serializers.ModelSerializer):
    """Presentation template serializer"""
    class Meta:
        model = PresentationTemplate
        fields = '__all__'
