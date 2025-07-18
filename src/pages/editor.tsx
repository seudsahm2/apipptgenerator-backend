import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import { Button } from "../components/ui/button"
import { Save, Download, Share, ArrowLeft } from "lucide-react"
import { Link } from "react-router-dom"

export default function Editor() {
  return (
    <div className="min-h-screen bg-muted/50">
      <header className="bg-background border-b">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <Link to="/dashboard">
              <Button variant="ghost" size="sm">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back to Dashboard
              </Button>
            </Link>
            <h1 className="text-xl font-semibold">Presentation Editor</h1>
          </div>
          <div className="flex space-x-2">
            <Button variant="outline" size="sm">
              <Save className="mr-2 h-4 w-4" />
              Save
            </Button>
            <Button variant="outline" size="sm">
              <Share className="mr-2 h-4 w-4" />
              Share
            </Button>
            <Button size="sm">
              <Download className="mr-2 h-4 w-4" />
              Export
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <Card>
          <CardHeader>
            <CardTitle>Editor Interface Coming Soon</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">The presentation editor will be implemented in Module 4 with:</p>
            <ul className="list-disc list-inside space-y-2 text-sm text-muted-foreground">
              <li>Drag-and-drop functionality</li>
              <li>Real-time collaboration</li>
              <li>AI-powered design suggestions</li>
              <li>WYSIWYG editing</li>
              <li>Export to PPTX/PDF</li>
            </ul>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
