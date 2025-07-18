"use client"

import type React from "react"
import { createContext, useContext, useState } from "react"

type Route = "/" | "/login" | "/dashboard" | "/editor"

interface NavigationContextType {
  currentRoute: Route
  navigate: (route: Route) => void
  params: Record<string, string>
}

const NavigationContext = createContext<NavigationContextType | undefined>(undefined)

export function NavigationProvider({ children }: { children: React.ReactNode }) {
  const [currentRoute, setCurrentRoute] = useState<Route>("/")
  const [params, setParams] = useState<Record<string, string>>({})

  const navigate = (route: Route, routeParams?: Record<string, string>) => {
    setCurrentRoute(route)
    if (routeParams) {
      setParams(routeParams)
    } else {
      setParams({})
    }
  }

  const value = {
    currentRoute,
    navigate,
    params,
  }

  return <NavigationContext.Provider value={value}>{children}</NavigationContext.Provider>
}

export function useNavigation() {
  const context = useContext(NavigationContext)
  if (context === undefined) {
    throw new Error("useNavigation must be used within a NavigationProvider")
  }
  return context
}

// Link component to replace react-router Link
export function Link({
  to,
  children,
  className,
}: {
  to: Route
  children: React.ReactNode
  className?: string
}) {
  const { navigate } = useNavigation()

  return (
    <button onClick={() => navigate(to)} className={className}>
      {children}
    </button>
  )
}
