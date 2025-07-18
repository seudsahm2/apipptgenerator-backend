import { appConfig, features, uiConfig, rateLimitConfig, authConfig } from "./env"

export const APP_CONFIG = {
  name: appConfig.name,
  description: appConfig.description,
  version: appConfig.version,
  url: appConfig.url,
  author: "SlideCraft Team",
} as const

export const API_ENDPOINTS = {
  auth: {
    signup: "/auth/signup/",
    login: "/auth/login/",
    logout: "/auth/logout/",
    session: "/auth/session/",
    profile: "/auth/profile/",
  },
  presentations: {
    list: "/presentations/",
    create: "/presentations/",
    get: (id: string) => `/presentations/${id}/`,
    update: (id: string) => `/presentations/${id}/`,
    delete: (id: string) => `/presentations/${id}/`,
    duplicate: (id: string) => `/presentations/${id}/duplicate/`,
    slides: (id: string) => `/presentations/${id}/slides/`,
  },
  ai: {
    generate: "/generate/",
    status: "/generate/status/",
    regenerateSlide: (id: string) => `/generate/slide/${id}/regenerate/`,
    enhance: "/generate/presentation/enhance/",
  },
  export: {
    pptx: "/export/pptx/",
    pdf: "/export/pdf/",
    formats: "/export/formats/",
  },
  core: {
    health: "/health/",
    status: "/health/status/",
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
  authToken: authConfig.cookieName + "-token",
  theme: "slidecraft-theme-preference",
  recentPresentations: "slidecraft-recent-presentations",
  userPreferences: "slidecraft-user-preferences",
} as const

export const FEATURE_FLAGS = {
  analytics: features.analytics,
  errorReporting: features.errorReporting,
  collaboration: features.collaboration,
  exportPDF: features.exportPDF,
  exportPPTX: features.exportPPTX,
  devTools: features.devTools,
  debugInfo: features.debugInfo,
} as const

export const RATE_LIMITS = {
  requests: rateLimitConfig.requests,
  window: rateLimitConfig.window,
} as const

export const DEFAULT_PRESENTATION_CONFIG = {
  slideCount: SLIDE_LIMITS.default,
  theme: "professional",
  template: "default",
} as const
