import { z } from "zod"

// Environment variable schema validation
const envSchema = z.object({
  // App Configuration
  VITE_APP_NAME: z.string().default("SlideCraft AI"),
  VITE_APP_VERSION: z.string().default("1.0.0"),
  VITE_APP_DESCRIPTION: z.string().default("AI-Powered PowerPoint Generation Platform"),
  VITE_APP_URL: z.string().url().default("http://localhost:3000"),

  // API Configuration
  VITE_API_URL: z.string().url().default("http://localhost:3001"),
  VITE_API_TIMEOUT: z.string().transform(Number).default("30000"),

  // OpenAI Configuration
  VITE_OPENAI_API_KEY: z.string().optional(),
  VITE_OPENAI_MODEL: z.string().default("gpt-4"),
  VITE_OPENAI_IMAGE_MODEL: z.string().default("dall-e-3"),
  VITE_OPENAI_MAX_TOKENS: z.string().transform(Number).default("4000"),
  VITE_OPENAI_TEMPERATURE: z.string().transform(Number).default("0.7"),

  // Authentication
  VITE_AUTH_COOKIE_NAME: z.string().default("slidecraft-auth"),
  VITE_AUTH_SESSION_TIMEOUT: z.string().transform(Number).default("86400000"),
  VITE_AUTH_REMEMBER_ME_TIMEOUT: z.string().transform(Number).default("2592000000"),

  // Feature Flags
  VITE_ENABLE_ANALYTICS: z
    .string()
    .transform((val) => val === "true")
    .default("false"),
  VITE_ENABLE_ERROR_REPORTING: z
    .string()
    .transform((val) => val === "true")
    .default("false"),
  VITE_ENABLE_COLLABORATION: z
    .string()
    .transform((val) => val === "true")
    .default("false"),
  VITE_ENABLE_EXPORT_PDF: z
    .string()
    .transform((val) => val === "true")
    .default("true"),
  VITE_ENABLE_EXPORT_PPTX: z
    .string()
    .transform((val) => val === "true")
    .default("true"),

  // Analytics
  VITE_GOOGLE_ANALYTICS_ID: z.string().optional(),
  VITE_SENTRY_DSN: z.string().optional(),
  VITE_HOTJAR_ID: z.string().optional(),

  // Storage
  VITE_FIREBASE_API_KEY: z.string().optional(),
  VITE_FIREBASE_AUTH_DOMAIN: z.string().optional(),
  VITE_FIREBASE_PROJECT_ID: z.string().optional(),
  VITE_FIREBASE_STORAGE_BUCKET: z.string().optional(),

  // Social Auth
  VITE_GOOGLE_CLIENT_ID: z.string().optional(),
  VITE_GITHUB_CLIENT_ID: z.string().optional(),

  // Development
  VITE_DEV_MODE: z
    .string()
    .transform((val) => val === "true")
    .default("false"),
  VITE_DEBUG_MODE: z
    .string()
    .transform((val) => val === "true")
    .default("false"),
  VITE_MOCK_API: z
    .string()
    .transform((val) => val === "true")
    .default("false"),

  // Rate Limiting
  VITE_RATE_LIMIT_REQUESTS: z.string().transform(Number).default("100"),
  VITE_RATE_LIMIT_WINDOW: z.string().transform(Number).default("900000"),

  // UI Configuration
  VITE_DEFAULT_THEME: z.enum(["light", "dark", "system"]).default("system"),
  VITE_PRIMARY_COLOR: z.string().default("#6366f1"),
  VITE_BRAND_NAME: z.string().default("SlideCraft AI"),
})

// Validate and parse environment variables
function validateEnv() {
  try {
    return envSchema.parse(import.meta.env)
  } catch (error) {
    console.error("❌ Invalid environment variables:", error)
    throw new Error("Invalid environment configuration")
  }
}

// Export validated environment configuration
export const env = validateEnv()

// Environment utilities
export const isDevelopment = env.VITE_DEV_MODE
export const isProduction = !env.VITE_DEV_MODE
export const isDebugMode = env.VITE_DEBUG_MODE

// API Configuration
export const apiConfig = {
  baseURL: env.VITE_API_URL,
  timeout: env.VITE_API_TIMEOUT,
  mockAPI: env.VITE_MOCK_API,
}

// OpenAI Configuration
export const openaiConfig = {
  apiKey: env.VITE_OPENAI_API_KEY,
  model: env.VITE_OPENAI_MODEL,
  imageModel: env.VITE_OPENAI_IMAGE_MODEL,
  maxTokens: env.VITE_OPENAI_MAX_TOKENS,
  temperature: env.VITE_OPENAI_TEMPERATURE,
}

// Feature flags
export const features = {
  analytics: env.VITE_ENABLE_ANALYTICS,
  errorReporting: env.VITE_ENABLE_ERROR_REPORTING,
  collaboration: env.VITE_ENABLE_COLLABORATION,
  exportPDF: env.VITE_ENABLE_EXPORT_PDF,
  exportPPTX: env.VITE_ENABLE_EXPORT_PPTX,
}

// Firebase configuration
export const firebaseConfig = {
  apiKey: env.VITE_FIREBASE_API_KEY,
  authDomain: env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: env.VITE_FIREBASE_STORAGE_BUCKET,
}

// Analytics configuration
export const analyticsConfig = {
  googleAnalyticsId: env.VITE_GOOGLE_ANALYTICS_ID,
  sentryDsn: env.VITE_SENTRY_DSN,
  hotjarId: env.VITE_HOTJAR_ID,
}

// Social auth configuration
export const socialAuthConfig = {
  googleClientId: env.VITE_GOOGLE_CLIENT_ID,
  githubClientId: env.VITE_GITHUB_CLIENT_ID,
}

// Rate limiting configuration
export const rateLimitConfig = {
  requests: env.VITE_RATE_LIMIT_REQUESTS,
  window: env.VITE_RATE_LIMIT_WINDOW,
}

// UI configuration
export const uiConfig = {
  defaultTheme: env.VITE_DEFAULT_THEME,
  primaryColor: env.VITE_PRIMARY_COLOR,
  brandName: env.VITE_BRAND_NAME,
}

// App metadata
export const appConfig = {
  name: env.VITE_APP_NAME,
  version: env.VITE_APP_VERSION,
  description: env.VITE_APP_DESCRIPTION,
  url: env.VITE_APP_URL,
}
