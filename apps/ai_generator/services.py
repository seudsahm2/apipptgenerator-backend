import openai
from django.conf import settings
from typing import Dict, List, Any
import json
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    """OpenAI API service for generating presentations"""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.image_model = settings.OPENAI_IMAGE_MODEL
        self.max_tokens = int(settings.OPENAI_MAX_TOKENS)
        self.temperature = float(settings.OPENAI_TEMPERATURE)
    
    def generate_presentation_content(self, topic: str, slide_count: int) -> Dict[str, Any]:
        """Generate presentation content using OpenAI"""
        try:
            prompt = self._create_presentation_prompt(topic, slide_count)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert presentation creator. Generate professional, engaging presentation content in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error generating presentation content: {str(e)}")
            raise Exception(f"Failed to generate presentation: {str(e)}")
    
    def generate_slide_image(self, image_prompt: str) -> str:
        """Generate image for a slide using DALL-E"""
        try:
            response = openai.Image.create(
                model=self.image_model,
                prompt=f"Professional presentation slide image: {image_prompt}. Clean, modern, business-appropriate style.",
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            return response.data[0].url
            
        except Exception as e:
            logger.error(f"Error generating slide image: {str(e)}")
            return None
    
    def _create_presentation_prompt(self, topic: str, slide_count: int) -> str:
        """Create the prompt for presentation generation"""
        return f"""
        Generate a {slide_count}-slide presentation about "{topic}". 
        
        Return a JSON object with this exact structure:
        {{
            "title": "Presentation Title",
            "description": "Brief description of the presentation",
            "slides": [
                {{
                    "slide_number": 1,
                    "title": "Slide Title",
                    "content": "Slide content with 3 bullet points (max 12 words each)",
                    "image_prompt": "Description for generating a relevant image"
                }}
            ]
        }}
        
        Requirements:
        - Each slide must have exactly 3 bullet points
        - Each bullet point must be maximum 12 words
        - Content should be professional and engaging
        - Image prompts should describe relevant, professional images
        - First slide should be a title slide
        - Last slide should be a conclusion/thank you slide
        - Middle slides should cover key aspects of the topic
        
        Topic: {topic}
        Number of slides: {slide_count}
        """

# Initialize the service
openai_service = OpenAIService()
