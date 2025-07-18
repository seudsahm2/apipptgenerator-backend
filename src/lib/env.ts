import { z } from "zod"

// Environment variable schema validation
const envSchema = z.object({
  // App Configuration
  NEXT_PUBLIC_APP_NAME: z.string().default("SlideCraft AI"),
  NEXT_PUBLIC_APP_VERSION: z.string().default("1.0.0"),
  NEXT_PUBLIC_APP_DESCRIPTION: z.string().default("AI-Powered PowerPoint Generation Platform"),
  NEXT_PUBLIC_APP_URL: z.string().url().default("http://localhost:3000"),

  // API Configuration
  NEXT_PUBLIC_API_URL: z.string().url().default("http://localhost:8000"),
  NEXT_PUBLIC_API_TIMEOUT: z.string().transform(Number).default("30000"),

  // Authentication
  NEXT_PUBLIC_AUTH_COOKIE_NAME: z.string().default("slidecraft-auth"),
  NEXT_PUBLIC_AUTH_SESSION_TIMEOUT: z.string().transform(Number).default("86400000"),
  NEXT_PUBLIC_AUTH_REMEMBER_ME_TIMEOUT: z.string().transform(Number).default("2592000000"),

  // Feature Flags
  NEXT_PUBLIC_ENABLE_ANALYTICS: z
    .string()
    .transform((val) => val === "true")
    .default("false"),
  NEXT_PUBLIC_ENABLE_ERROR_REPORTING: z
    .string()
    .transform((val) => val === "true")
    .default("false"),
  NEXT_PUBLIC_ENABLE_COLLABORATION: z
    .string()
    .transform((val) => val === "true")
    .default("false"),
  NEXT_PUBLIC_ENABLE_EXPORT_PDF: z
    .string()
    .transform((val) => val === "true")
    .default("true"),
  NEXT_PUBLIC_ENABLE_EXPORT_PPTX: z
    .string()
    .transform((val) => val === "true")
    .default("true"),

  // Analytics
  NEXT_PUBLIC_GOOGLE_ANALYTICS_ID: z.string().optional(),
  NEXT_PUBLIC_SENTRY_DSN: z.string().optional(),
  NEXT_PUBLIC_HOTJAR_ID: z.string().optional(),

  // Development
  NEXT_PUBLIC_DEV_MODE: z
    .string()
    .transform((val) => val === "true")
    .default("false"),
  NEXT_PUBLIC_DEBUG_MODE: z
    .string()
    .transform((val) => val === "true")
    .default("false"),
  NEXT_PUBLIC_MOCK_API: z
    .string()
    .transform((val) => val === "true")
    .default("false"),

  // Rate Limiting
  NEXT_PUBLIC_RATE_LIMIT_REQUESTS: z.string().transform(Number).default("100"),
  NEXT_PUBLIC_RATE_LIMIT_WINDOW: z.string().transform(Number).default("900000"),

  // UI Configuration
  NEXT_PUBLIC_DEFAULT_THEME: z.enum(["light", "dark", "system"]).default("system"),
  NEXT_PUBLIC_PRIMARY_COLOR: z.string().default("#6366f1"),
  NEXT_PUBLIC_BRAND_NAME: z.string().default("SlideCraft AI"),

  // AI Configuration (Display Only)
  NEXT_PUBLIC_AI_PROVIDER: z.string().default("Google Gemini"),
  NEXT_PUBLIC_AI_IS_FREE: z
    .string()
    .transform((val) => val === "true")
    .default("true"),
  NEXT_PUBLIC_AI_RATE_LIMIT: z.string().default("15 requests per minute"),

  // Development Tools
  NEXT_PUBLIC_ENABLE_DEV_TOOLS: z
    .string()
    .transform((val) => val === "true")
    .default("false"),
  NEXT_PUBLIC_SHOW_DEBUG_INFO: z
    .string()
    .transform((val) => val === "true")
    .default("false"),
})

// Validate and parse environment variables
function validateEnv() {
  try {
    return envSchema.parse(process.env)
  } catch (error) {
    console.error("❌ Invalid environment variables:", error)
    throw new Error("Invalid environment configuration")
  }
}

// Export validated environment configuration
export const env = validateEnv()

// Environment utilities
export const isDevelopment = env.NEXT_PUBLIC_DEV_MODE
export const isProduction = !env.NEXT_PUBLIC_DEV_MODE
export const isDebugMode = env.NEXT_PUBLIC_DEBUG_MODE

// API Configuration
export const apiConfig = {
  baseURL: env.NEXT_PUBLIC_API_URL,
  timeout: env.NEXT_PUBLIC_API_TIMEOUT,
  mockAPI: env.NEXT_PUBLIC_MOCK_API,
}

// Feature flags
export const features = {
  analytics: env.NEXT_PUBLIC_ENABLE_ANALYTICS,
  errorReporting: env.NEXT_PUBLIC_ENABLE_ERROR_REPORTING,
  collaboration: env.NEXT_PUBLIC_ENABLE_COLLABORATION,
  exportPDF: env.NEXT_PUBLIC_ENABLE_EXPORT_PDF,
  exportPPTX: env.NEXT_PUBLIC_ENABLE_EXPORT_PPTX,
  devTools: env.NEXT_PUBLIC_ENABLE_DEV_TOOLS,
  debugInfo: env.NEXT_PUBLIC_SHOW_DEBUG_INFO,
}

// Analytics configuration
export const analyticsConfig = {
  googleAnalyticsId: env.NEXT_PUBLIC_GOOGLE_ANALYTICS_ID,
  sentryDsn: env.NEXT_PUBLIC_SENTRY_DSN,
  hotjarId: env.NEXT_PUBLIC_HOTJAR_ID,
}

// Rate limiting configuration
export const rateLimitConfig = {
  requests: env.NEXT_PUBLIC_RATE_LIMIT_REQUESTS,
  window: env.NEXT_PUBLIC_RATE_LIMIT_WINDOW,
}

// UI configuration
export const uiConfig = {
  defaultTheme: env.NEXT_PUBLIC_DEFAULT_THEME,
  primaryColor: env.NEXT_PUBLIC_PRIMARY_COLOR,
  brandName: env.NEXT_PUBLIC_BRAND_NAME,
}

// App metadata
export const appConfig = {
  name: env.NEXT_PUBLIC_APP_NAME,
  version: env.NEXT_PUBLIC_APP_VERSION,
  description: env.NEXT_PUBLIC_APP_DESCRIPTION,
  url: env.NEXT_PUBLIC_APP_URL,
}

// AI configuration
export const aiConfig = {
  provider: env.NEXT_PUBLIC_AI_PROVIDER,
  isFree: env.NEXT_PUBLIC_AI_IS_FREE,
  rateLimit: env.NEXT_PUBLIC_AI_RATE_LIMIT,
}

// Auth configuration
export const authConfig = {
  cookieName: env.NEXT_PUBLIC_AUTH_COOKIE_NAME,
  sessionTimeout: env.NEXT_PUBLIC_AUTH_SESSION_TIMEOUT,
  rememberMeTimeout: env.NEXT_PUBLIC_AUTH_REMEMBER_ME_TIMEOUT,
}
