# Environment Variables Setup Guide

## Overview
SlideCraft AI uses environment variables for configuration across different environments (development, staging, production).

## Quick Setup

### 1. Copy Environment Files
\`\`\`bash
# For local development
cp .env.local.example .env.local

# For production (Vercel will handle this)
cp .env.example .env.production
\`\`\`

### 2. Configure Required Variables

#### Essential Variables (Required)
- \`VITE_APP_URL\` - Your application URL
- \`VITE_API_URL\` - Your backend API URL
- \`VITE_OPENAI_API_KEY\` - OpenAI API key for AI features

#### Optional Variables
- \`VITE_GOOGLE_ANALYTICS_ID\` - Google Analytics tracking
- \`VITE_SENTRY_DSN\` - Error reporting with Sentry
- \`VITE_FIREBASE_*\` - Firebase configuration for file storage

## Vercel Deployment Setup

### 1. Environment Variables in Vercel Dashboard

Go to your Vercel project → Settings → Environment Variables and add:

#### Production Environment
\`\`\`
VITE_APP_NAME=SlideCraft AI
VITE_APP_VERSION=1.0.0
VITE_APP_URL=https://your-domain.vercel.app
VITE_API_URL=https://your-backend-api.render.com
VITE_OPENAI_API_KEY=sk-your-production-openai-key
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_ERROR_REPORTING=true
VITE_GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
VITE_SENTRY_DSN=https://your-sentry-dsn@sentry.io/project
\`\`\`

#### Preview Environment (Optional)
\`\`\`
VITE_APP_NAME=SlideCraft AI (Preview)
VITE_API_URL=https://your-staging-api.render.com
VITE_OPENAI_API_KEY=sk-your-staging-openai-key
VITE_ENABLE_ANALYTICS=false
\`\`\`

### 2. Automatic Deployment
Once environment variables are set, Vercel will automatically use them during build and runtime.

## Local Development

### 1. Create .env.local
\`\`\`bash
# Copy the example file
cp .env.local.example .env.local
\`\`\`

### 2. Update with your values
\`\`\`env
VITE_API_URL=http://localhost:3001
VITE_OPENAI_API_KEY=sk-your-development-key
VITE_DEV_MODE=true
VITE_DEBUG_MODE=true
\`\`\`

### 3. Start development server
\`\`\`bash
npm run dev
\`\`\`

## Environment Validation

The application automatically validates environment variables on startup using Zod schema validation.

### Validation Features
- ✅ Type checking for all variables
- ✅ Default values for optional variables
- ✅ URL validation for API endpoints
- ✅ Boolean transformation for feature flags
- ✅ Number transformation for numeric values

### Validation Errors
If environment variables are invalid, you'll see detailed error messages in the console.

## Feature Flags

Control application features using environment variables:

\`\`\`env
VITE_ENABLE_ANALYTICS=true          # Google Analytics
VITE_ENABLE_ERROR_REPORTING=true    # Sentry error reporting
VITE_ENABLE_COLLABORATION=false     # Real-time collaboration
VITE_ENABLE_EXPORT_PDF=true         # PDF export functionality
VITE_ENABLE_EXPORT_PPTX=true        # PowerPoint export
\`\`\`

## Security Best Practices

### ✅ Do's
- Use different API keys for development/production
- Keep sensitive keys in Vercel environment variables
- Use feature flags to disable features in development
- Validate all environment variables

### ❌ Don'ts
- Never commit .env files to git
- Don't use production keys in development
- Don't expose sensitive data in client-side variables
- Don't hardcode configuration values

## Troubleshooting

### Common Issues

1. **Blank page on Vercel**
   - Check if all required environment variables are set
   - Verify API URLs are accessible
   - Check browser console for errors

2. **API connection errors**
   - Verify \`VITE_API_URL\` is correct
   - Check CORS configuration
   - Ensure backend is deployed and running

3. **Build failures**
   - Run \`npm run env:validate\` to check environment variables
   - Check TypeScript errors
   - Verify all dependencies are installed

### Debug Mode
Enable debug mode for detailed logging:
\`\`\`env
VITE_DEBUG_MODE=true
VITE_DEV_MODE=true
\`\`\`

## Environment Files Priority

1. \`.env.local\` (highest priority, git-ignored)
2. \`.env.production\` (production builds)
3. \`.env\` (default values)
4. \`.env.example\` (template only)
\`\`\`
\`\`\`

## Update .gitignore
