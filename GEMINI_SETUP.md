# Google Gemini API Setup Guide

## 🎉 **FREE AI-Powered Presentations with Google Gemini!**

Your SlideCraft AI backend now uses Google's **completely FREE** Gemini API instead of paid OpenAI services.

## 🔑 **Getting Your FREE Gemini API Key**

### Step 1: Visit Google AI Studio
1. Go to: **https://aistudio.google.com/**
2. Sign in with your Google account (free)

### Step 2: Create API Key
1. Click **"Get API Key"** in the top right
2. Click **"Create API Key"**
3. Select **"Create API key in new project"** (recommended)
4. Copy your API key (starts with `AIza...`)

### Step 3: Configure Environment Variables

#### For Render Deployment:
\`\`\`env
GEMINI_API_KEY=AIzaSyC-your-actual-api-key-here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=8192
GEMINI_TEMPERATURE=0.7
\`\`\`

#### For Local Development:
\`\`\`env
# .env file
GEMINI_API_KEY=AIzaSyC-your-actual-api-key-here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=8192
GEMINI_TEMPERATURE=0.7
DEBUG=True
\`\`\`

## 🚀 **API Endpoints**

All endpoints remain exactly the same:

\`\`\`
POST /api/generate/                    # Generate presentation
POST /api/generate/slide/{id}/regenerate/  # Regenerate slide content
POST /api/generate/presentation/enhance/   # Enhance presentation
GET  /api/generate/status/             # Check AI status
\`\`\`

## 🆓 **Gemini vs OpenAI Comparison**

| Feature | Google Gemini | OpenAI |
|---------|---------------|---------|
| **Cost** | **100% FREE** | $20+/month |
| **Rate Limits** | 15 requests/minute | 3 requests/minute |
| **Setup** | No credit card | Credit card required |
| **Model** | gemini-1.5-flash | gpt-4 |
| **Quality** | Excellent | Excellent |
| **Context** | 1M tokens | 128K tokens |

## 🔧 **Testing Your Setup**

### 1. Test API Status
\`\`\`bash
curl -X GET http://localhost:8000/api/generate/status/
\`\`\`

Should return:
\`\`\`json
{
  "ai_provider": "Google Gemini",
  "is_free": true,
  "gemini_configured": true,
  "model": "gemini-1.5-flash"
}
\`\`\`

### 2. Test Backend Endpoint
\`\`\`bash
curl -X GET http://localhost:8000/health/
\`\`\`

Should return:
\`\`\`json
{
  "status": "healthy",
  "ai_provider": "Google Gemini (Free)",
  "service": "SlideCraft AI Backend"
}
\`\`\`

## 🎯 **Benefits of Using Gemini**

### ✅ **Advantages:**
- **Completely FREE** - No usage costs ever
- **No Credit Card** - Just Google account needed
- **Higher Rate Limits** - 15 requests/minute vs 3
- **Large Context Window** - 1M tokens vs 128K
- **Fast Model** - gemini-1.5-flash is optimized for speed
- **JSON Mode** - Native JSON response support
- **Google Infrastructure** - Reliable and fast

### 🔄 **What Changed:**
- ❌ Removed `openai` dependency
- ✅ Added `google-generativeai` package
- ✅ Updated AI service to use Gemini
- ✅ Enhanced error handling and fallbacks
- ✅ Added retry logic for rate limits
- ✅ Same API endpoints and functionality

### 📊 **Features Available:**
- ✅ **Presentation Generation** - Full presentations from topics
- ✅ **Content Enhancement** - Improve existing presentations  
- ✅ **Slide Regeneration** - Regenerate individual slide content
- ✅ **Image Prompts** - Generate descriptions for images
- ✅ **Fallback Content** - Graceful handling if AI fails
- ✅ **Rate Limit Handling** - Automatic retry with backoff

## 🐛 **Troubleshooting**

### Common Issues:

1. **"API key not configured"**
   - Check your .env file has `GEMINI_API_KEY`
   - Verify the API key is correct (starts with `AIza`)

2. **"Rate limit exceeded"**
   - Wait 1 minute and try again
   - Free tier: 15 requests per minute

3. **"Invalid API key"**
   - Generate a new API key from Google AI Studio
   - Make sure you're using the correct project

### Debug Commands:
\`\`\`bash
# Check environment variables
python manage.py shell -c "from django.conf import settings; print(settings.GEMINI_API_KEY[:10] + '...')"

# Test AI generation
curl -X POST http://localhost:8000/api/generate/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-jwt-token" \
  -d '{"topic": "Test Topic", "slideCount": 3}'
\`\`\`

## 🌟 **Production Deployment**

### Render Environment Variables:
\`\`\`
GEMINI_API_KEY=AIzaSyC-your-actual-api-key-here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=8192
GEMINI_TEMPERATURE=0.7
\`\`\`

### Vercel Frontend Environment Variables:
\`\`\`
NEXT_PUBLIC_API_URL=https://your-render-app.onrender.com
\`\`\`

## 🎉 **Success!**

Your SlideCraft AI is now powered by **FREE Google Gemini AI**! 

- ✅ No monthly costs
- ✅ No credit card required  
- ✅ Higher rate limits
- ✅ Same great functionality
- ✅ Production ready

**Total cost to run SlideCraft AI: $0.00** 🎉
