"use client"

import type React from "react"
import { createContext, useContext, useEffect, useState } from "react"
import { api } from "../lib/axios"
import { STORAGE_KEYS } from "../lib/constants"

interface User {
  id: string
  email: string
  name: string
  createdAt: string
}

interface AuthContextType {
  user: User | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  signup: (email: string, password: string, name: string) => Promise<void>
  logout: () => Promise<void>
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const checkSession = async () => {
    try {
      const response = await api.get("/auth/session")
      setUser(response.data.user)
    } catch (error) {
      console.error("Session check failed:", error)
      localStorage.removeItem(STORAGE_KEYS.authToken)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    const token = localStorage.getItem(STORAGE_KEYS.authToken)
    if (token) {
      checkSession()
    } else {
      setIsLoading(false)
    }
  }, [])

  const login = async (email: string, password: string) => {
    const response = await api.post("/auth/login", { email, password })
    const { user, token } = response.data

    localStorage.setItem(STORAGE_KEYS.authToken, token)
    setUser(user)
  }

  const signup = async (email: string, password: string, name: string) => {
    const response = await api.post("/auth/signup", { email, password, name })
    const { user, token } = response.data

    localStorage.setItem(STORAGE_KEYS.authToken, token)
    setUser(user)
  }

  const logout = async () => {
    try {
      await api.get("/auth/logout")
    } catch (error) {
      console.error("Logout error:", error)
    } finally {
      localStorage.removeItem(STORAGE_KEYS.authToken)
      setUser(null)
    }
  }

  const value = {
    user,
    isLoading,
    login,
    signup,
    logout,
    isAuthenticated: !!user,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
