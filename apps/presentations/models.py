from django.db import models
from django.contrib.auth import get_user_model
import uuid
import json

User = get_user_model()

class Presentation(models.Model):
    """Presentation model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='presentations')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    topic = models.CharField(max_length=500)
    slide_count = models.IntegerField(default=5)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    thumbnail = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'presentations'
        ordering = ['-created_at']
        verbose_name = 'Presentation'
        verbose_name_plural = 'Presentations'
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"

class Slide(models.Model):
    """Individual slide model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name='slides')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    image_prompt = models.TextField(blank=True)
    slide_number = models.IntegerField()
    background_color = models.CharField(max_length=7, default='#ffffff')
    text_color = models.CharField(max_length=7, default='#000000')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'slides'
        ordering = ['slide_number']
        unique_together = ['presentation', 'slide_number']
        verbose_name = 'Slide'
        verbose_name_plural = 'Slides'
    
    def __str__(self):
        return f"Slide {self.slide_number}: {self.title}"

class PresentationTemplate(models.Model):
    """Presentation template model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.URLField()
    template_data = models.JSONField(default=dict)
    is_premium = models.BooleanField(default=False)
    category = models.CharField(max_length=100, default='business')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'presentation_templates'
        verbose_name = 'Presentation Template'
        verbose_name_plural = 'Presentation Templates'
    
    def __str__(self):
        return self.name
