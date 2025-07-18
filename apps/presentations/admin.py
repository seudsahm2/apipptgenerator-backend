from django.contrib import admin
from .models import Presentation, Slide, PresentationTemplate

@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'slide_count', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'user__email', 'topic')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'presentation', 'slide_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'presentation__title')

@admin.register(PresentationTemplate)
class PresentationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_premium', 'created_at')
    list_filter = ('category', 'is_premium', 'created_at')
    search_fields = ('name', 'description')
