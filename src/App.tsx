import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import { QueryProvider } from "./providers/query-provider"
import { AuthProvider } from "./providers/auth-provider"
import { ThemeProvider } from "./providers/theme-provider"
import ErrorBoundary from "./components/error-boundary"
import "./styles/globals.css"

// Direct imports instead of lazy loading for better reliability
import Landing from "./pages/landing"
import Auth from "./pages/auth"
import Dashboard from "./pages/dashboard"
import Editor from "./pages/editor"

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="system">
        <QueryProvider>
          <AuthProvider>
            <Router>
              <div className="min-h-screen bg-background text-foreground">
                <Routes>
                  <Route path="/" element={<Landing />} />
                  <Route path="/auth" element={<Auth />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/editor/:id?" element={<Editor />} />
                </Routes>
              </div>
            </Router>
          </AuthProvider>
        </QueryProvider>
      </ThemeProvider>
    </ErrorBoundary>
  )
}

export default App
