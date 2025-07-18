"use client"

import { QueryProvider } from "../providers/query-provider"
import { AuthProvider } from "../providers/auth-provider"
import { ThemeProvider } from "../providers/theme-provider"
import { NavigationProvider, useNavigation } from "../providers/navigation-provider"
import { Skeleton } from "../components/ui/skeleton"

// Import pages
import Dashboard from "../pages/dashboard"
import Login from "../pages/login"
import Editor from "../pages/editor"
import Landing from "../pages/landing"

function LoadingFallback() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="space-y-4 w-full max-w-md">
        <Skeleton className="h-8 w-full" />
        <Skeleton className="h-4 w-3/4" />
        <Skeleton className="h-4 w-1/2" />
      </div>
    </div>
  )
}

function AppRouter() {
  const { currentRoute } = useNavigation()

  switch (currentRoute) {
    case "/":
      return <Landing />
    case "/login":
      return <Login />
    case "/dashboard":
      return <Dashboard />
    case "/editor":
      return <Editor />
    default:
      return <Landing />
  }
}

export default function AppShell() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="theme-preference">
      <QueryProvider>
        <AuthProvider>
          <NavigationProvider>
            <div className="min-h-screen bg-background text-foreground">
              <AppRouter />
            </div>
          </NavigationProvider>
        </AuthProvider>
      </QueryProvider>
    </ThemeProvider>
  )
}
