import axios from "axios"
import { apiConfig, isDevelopment } from "./env"
import { STORAGE_KEYS } from "./constants"

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:3001"

export const api = axios.create({
  baseURL: `${apiConfig.baseURL}/api`,
  timeout: apiConfig.timeout,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(STORAGE_KEYS.authToken)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    // Add environment info in development
    if (isDevelopment) {
      config.headers["X-Environment"] = "development"
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    // Log API responses in development
    if (isDevelopment) {
      console.log("API Response:", response.config.url, response.status)
    }
    return response
  },
  (error) => {
    // Enhanced error logging
    if (isDevelopment) {
      console.error("API Error:", error.config?.url, error.response?.status, error.message)
    }

    if (error.response?.status === 401) {
      localStorage.removeItem(STORAGE_KEYS.authToken)
      window.location.href = "/auth"
    }
    return Promise.reject(error)
  },
)

export default api
