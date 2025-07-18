import { appConfig, features, uiConfig, rateLimitConfig } from "./env"

export const APP_CONFIG = {
  name: appConfig.name,
  description: appConfig.description,
  version: appConfig.version,
  url: appConfig.url,
  author: "SlideCraft Team",
} as const

export const API_ENDPOINTS = {
  auth: {
    signup: "/auth/signup",
    login: "/auth/login",
    logout: "/auth/logout",
    session: "/auth/session",
  },
  presentations: {
    generate: "/generate",
    list: "/presentations",
    get: (id: string) => `/presentations/${id}`,
    update: (id: string) => `/presentations/${id}`,
    delete: (id: string) => `/presentations/${id}`,
  },
  export: {
    pptx: "/export/pptx",
    pdf: "/export/pdf",
  },
} as const

export const SLIDE_LIMITS = {
  min: 3,
  max: 10,
  default: 5,
} as const

export const THEME_COLORS = {
  primary: uiConfig.primaryColor,
  secondary: "#8b5cf6",
  accent: "#06b6d4",
  success: "#10b981",
  warning: "#f59e0b",
  error: "#ef4444",
} as const

export const STORAGE_KEYS = {
  authToken: "slidecraft-auth-token",
  theme: "slidecraft-theme-preference",
  recentPresentations: "slidecraft-recent-presentations",
} as const

export const FEATURE_FLAGS = {
  analytics: features.analytics,
  errorReporting: features.errorReporting,
  collaboration: features.collaboration,
  exportPDF: features.exportPDF,
  exportPPTX: features.exportPPTX,
} as const

export const RATE_LIMITS = {
  requests: rateLimitConfig.requests,
  window: rateLimitConfig.window,
} as const
