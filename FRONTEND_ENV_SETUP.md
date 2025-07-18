# Frontend Environment Variables Setup Guide

## 🎯 **Quick Setup for Your Deployed Backend**

Your Django backend is deployed at: `https://apipptgenerator-backend.onrender.com`

### 1. For Local Development (.env.local)
\`\`\`env
NEXT_PUBLIC_API_URL="http://localhost:8000"
NEXT_PUBLIC_DEV_MODE="true"
NEXT_PUBLIC_DEBUG_MODE="true"
\`\`\`

### 2. For Production (.env.production)
\`\`\`env
NEXT_PUBLIC_API_URL="https://apipptgenerator-backend.onrender.com"
NEXT_PUBLIC_DEV_MODE="false"
NEXT_PUBLIC_DEBUG_MODE="false"
\`\`\`

## 🚀 **Vercel Deployment Environment Variables**

In your Vercel dashboard, add these environment variables:

### Required Variables:
\`\`\`
NEXT_PUBLIC_API_URL=https://apipptgenerator-backend.onrender.com
NEXT_PUBLIC_APP_URL=https://your-frontend-domain.vercel.app
NEXT_PUBLIC_DEV_MODE=false
NEXT_PUBLIC_DEBUG_MODE=false
\`\`\`

### Optional Variables:
\`\`\`
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_ERROR_REPORTING=true
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
NEXT_PUBLIC_SENTRY_DSN=https://your-sentry-dsn@sentry.io/project
\`\`\`

## 🔧 **Testing Your Setup**

### 1. Test Backend Connection
\`\`\`bash
# In your frontend project
npm run dev

# Check browser console for:
# ✅ API Response: /health/ 200
\`\`\`

### 2. Test API Endpoints
\`\`\`javascript
// In browser console
fetch('https://apipptgenerator-backend.onrender.com/health/')
  .then(r => r.json())
  .then(console.log)

// Should return:
// { status: "healthy", ai_provider: "Google Gemini (Free)" }
\`\`\`

## 📁 **File Structure**
\`\`\`
src/
├── lib/
│   ├── env.ts          # Environment validation
│   ├── axios.ts        # API client with your backend URL
│   └── constants.ts    # API endpoints and config
├── .env.local          # Local development
├── .env.production     # Production build
└── vercel.json         # Vercel deployment config
\`\`\`

## 🎯 **Key Features Configured**

### ✅ **API Integration**
- Backend URL: `https://apipptgenerator-backend.onrender.com`
- Authentication with JWT tokens
- Error handling and retries
- CORS configuration

### ✅ **Feature Flags**
- Free AI with Google Gemini
- PDF/PPTX export enabled
- Development tools in dev mode
- Analytics ready for production

### ✅ **Environment Validation**
- Zod schema validation
- Type-safe environment variables
- Fallback values for missing vars
- Development vs production configs

## 🚨 **Important Notes**

1. **Backend URL**: Make sure your backend is deployed and accessible
2. **CORS**: Your backend should allow your frontend domain
3. **Authentication**: JWT tokens are stored in localStorage
4. **Rate Limiting**: 15 requests/minute for free Gemini API

## 🐛 **Troubleshooting**

### Common Issues:

1. **CORS Error**
   - Check backend ALLOWED_HOSTS includes your domain
   - Verify CORS_ALLOWED_ORIGINS in Django settings

2. **API Connection Failed**
   - Verify backend is running: `https://apipptgenerator-backend.onrender.com/health/`
   - Check NEXT_PUBLIC_API_URL is correct

3. **Environment Variables Not Loading**
   - Restart development server after changing .env files
   - Check variable names start with NEXT_PUBLIC_

### Debug Commands:
\`\`\`bash
# Check environment variables
npm run dev
# Look for console logs showing loaded config

# Test API connection
curl https://apipptgenerator-backend.onrender.com/health/
\`\`\`

## 🎉 **Ready to Deploy!**

Your frontend is now configured to work with your free Django backend powered by Google Gemini AI!

**Total cost: $0.00** 🎉
