import { Link } from "react-router-dom"
import { Button } from "../components/ui/button"
import { Card, CardDescription, CardHeader, CardTitle } from "../components/ui/card"
import { Sparkles, Zap, Users, Presentation } from "lucide-react"

export default function Landing() {
  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Presentation className="h-8 w-8 text-primary" />
            <span className="text-2xl font-bold">SlideCraft AI</span>
          </div>
          <div className="flex items-center space-x-4">
            <Link to="/auth">
              <Button variant="ghost">Sign In</Button>
            </Link>
            <Link to="/auth">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 text-center">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
            AI-Powered PowerPoint Generation
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-3xl mx-auto">
            Transform your ideas into professional presentations in minutes. Powered by OpenAI GPT-4 and DALL-E for
            intelligent content generation and stunning visuals.
          </p>
          <Link to="/auth">
            <Button size="lg" className="text-lg px-8 py-4">
              Start Creating <Sparkles className="ml-2 h-6 w-6" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 bg-muted/50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12">Why Choose SlideCraft AI?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <Card>
              <CardHeader className="text-center">
                <Zap className="h-12 w-12 text-primary mb-4 mx-auto" />
                <CardTitle>Lightning Fast</CardTitle>
                <CardDescription>
                  Generate complete presentations in seconds with AI-powered content creation
                </CardDescription>
              </CardHeader>
            </Card>
            <Card>
              <CardHeader className="text-center">
                <Sparkles className="h-12 w-12 text-primary mb-4 mx-auto" />
                <CardTitle>AI-Powered</CardTitle>
                <CardDescription>
                  Advanced OpenAI integration creates intelligent content and stunning visuals
                </CardDescription>
              </CardHeader>
            </Card>
            <Card>
              <CardHeader className="text-center">
                <Users className="h-12 w-12 text-primary mb-4 mx-auto" />
                <CardTitle>Collaborative</CardTitle>
                <CardDescription>Real-time collaboration with your team members and instant sharing</CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container mx-auto px-4 text-center text-muted-foreground">
          <p>&copy; 2024 SlideCraft AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
