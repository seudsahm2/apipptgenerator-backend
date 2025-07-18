import google.generativeai as genai
from django.conf import settings
from typing import Dict, List, Any
import json
import logging
import time
import random

logger = logging.getLogger(__name__)

class GeminiService:
    """Google Gemini API service for generating presentations (FREE)"""
    
    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.GEMINI_MODEL
        self.max_tokens = int(settings.GEMINI_MAX_TOKENS)
        self.temperature = float(settings.GEMINI_TEMPERATURE)
        
        # Initialize the model with compatible configuration
        try:
            # Try with response_mime_type (newer versions)
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature,
                    response_mime_type="application/json"
                )
            )
        except TypeError:
            # Fallback for older versions without response_mime_type
            logger.info("Using fallback Gemini configuration (older API version)")
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature
                )
            )
    
    def generate_presentation_content(self, topic: str, slide_count: int) -> Dict[str, Any]:
        """Generate presentation content using Google Gemini (FREE)"""
        try:
            prompt = self._create_presentation_prompt(topic, slide_count)
            
            # Add retry logic for rate limiting
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.model.generate_content(prompt)
                    
                    if response.text:
                        # Try to parse as JSON
                        try:
                            content = json.loads(response.text)
                            return content
                        except json.JSONDecodeError:
                            # If not valid JSON, try to extract JSON from response
                            text = response.text.strip()
                            if text.startswith('```json'):
                                text = text.replace('```json', '').replace('```', '').strip()
                            elif text.startswith('```'):
                                text = text.replace('```', '').strip()
                            
                            try:
                                content = json.loads(text)
                                return content
                            except json.JSONDecodeError:
                                logger.warning("Could not parse JSON response, using fallback")
                                return self._create_fallback_content(topic, slide_count)
                    else:
                        raise Exception("Empty response from Gemini")
                        
                except Exception as e:
                    if "quota" in str(e).lower() or "rate" in str(e).lower():
                        if attempt < max_retries - 1:
                            # Wait with exponential backoff
                            wait_time = (2 ** attempt) + random.uniform(0, 1)
                            logger.warning(f"Rate limit hit, waiting {wait_time:.2f}s before retry {attempt + 1}")
                            time.sleep(wait_time)
                            continue
                    raise e
            
            raise Exception("Max retries exceeded")
            
        except Exception as e:
            logger.error(f"Error generating presentation content: {str(e)}")
            # Return fallback content instead of failing
            return self._create_fallback_content(topic, slide_count)
    
    def generate_slide_image_prompt(self, slide_title: str, slide_content: str) -> str:
        """Generate image prompt for slide (since Gemini doesn't generate images directly)"""
        try:
            prompt = f"""
            Create a detailed image description for a professional presentation slide.
            
            Slide Title: {slide_title}
            Slide Content: {slide_content}
            
            Generate a description for a professional, clean, modern image that would complement this slide.
            The description should be suitable for image generation tools.
            Keep it under 100 words and focus on professional business imagery.
            
            Return only the image description, nothing else.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip() if response.text else f"Professional illustration related to {slide_title}"
            
        except Exception as e:
            logger.error(f"Error generating image prompt: {str(e)}")
            return f"Professional business illustration about {slide_title}"
    
    def enhance_presentation_content(self, presentation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance existing presentation content"""
        try:
            prompt = f"""
            Enhance the following presentation content to make it more engaging and professional:
            
            {json.dumps(presentation_data, indent=2)}
            
            Improve the content while maintaining the same structure. Make bullet points more impactful,
            improve titles, and ensure professional language throughout.
            
            Return the enhanced content in the same JSON format.
            """
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                try:
                    enhanced_content = json.loads(response.text)
                    return enhanced_content
                except json.JSONDecodeError:
                    logger.warning("Could not parse enhanced content JSON")
                    return presentation_data
            else:
                return presentation_data
                
        except Exception as e:
            logger.error(f"Error enhancing presentation: {str(e)}")
            return presentation_data
    
    def _create_presentation_prompt(self, topic: str, slide_count: int) -> str:
        """Create the prompt for presentation generation"""
        return f"""
        Generate a professional {slide_count}-slide presentation about "{topic}".
        
        You MUST return a valid JSON object with this EXACT structure:
        {{
            "title": "Professional presentation title about {topic}",
            "description": "Brief 1-2 sentence description",
            "slides": [
                {{
                    "slide_number": 1,
                    "title": "Introduction to {topic}",
                    "content": "• First key point (max 12 words)\\n• Second key point (max 12 words)\\n• Third key point (max 12 words)",
                    "image_prompt": "Professional image description"
                }}
            ]
        }}
        
        CRITICAL REQUIREMENTS:
        - Generate exactly {slide_count} slides
        - Each slide must have exactly 3 bullet points
        - Each bullet point maximum 12 words
        - First slide: Title/Introduction slide
        - Last slide: Conclusion/Thank you slide
        - Middle slides: Key topics about {topic}
        - Professional, business-appropriate content
        - Image prompts should describe professional, clean imagery
        - Return ONLY valid JSON, no markdown formatting, no extra text
        
        Topic: {topic}
        Slide count: {slide_count}
        """
    
    def _create_fallback_content(self, topic: str, slide_count: int) -> Dict[str, Any]:
        """Create fallback content if AI generation fails"""
        slides = []
        
        # Title slide
        slides.append({
            "slide_number": 1,
            "title": f"Introduction to {topic}",
            "content": f"• Overview of {topic}\n• Key concepts and importance\n• What we'll cover today",
            "image_prompt": f"Professional illustration representing {topic}"
        })
        
        # Content slides
        for i in range(2, slide_count):
            slides.append({
                "slide_number": i,
                "title": f"{topic} - Key Point {i-1}",
                "content": f"• Important aspect of {topic}\n• Detailed explanation and benefits\n• Real-world applications",
                "image_prompt": f"Business chart or diagram about {topic}"
            })
        
        # Conclusion slide
        slides.append({
            "slide_number": slide_count,
            "title": "Conclusion",
            "content": f"• Summary of {topic} key points\n• Next steps and recommendations\n• Thank you for your attention",
            "image_prompt": "Professional thank you or conclusion image"
        })
        
        return {
            "title": f"Presentation: {topic}",
            "description": f"A comprehensive overview of {topic} and its key aspects.",
            "slides": slides
        }

# Initialize the service
gemini_service = GeminiService()
