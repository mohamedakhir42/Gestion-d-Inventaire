import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import { useAuth } from "@/contexts/auth-context"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertMessage } from "@/components/ui/alert"

export function LoginPage() {
  const navigate = useNavigate()
  const { login, loading } = useAuth()
  const [email, setEmail] = useState("admin@example.com")
  const [password, setPassword] = useState("password")
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    try {
      await login(email, password)
      navigate("/dashboard")
    } catch (err) {
      setError("Invalid email or password")
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 to-primary/10 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-primary mb-2">InventoryPro</h1>
          <p className="text-muted">Industrial Inventory Management System</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Sign in to your account</CardTitle>
            <CardDescription>Enter your credentials to continue</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && <AlertMessage variant="destructive" message={error} />}

              <div className="space-y-2">
                <Label htmlFor="email" required>
                  Email Address
                </Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={loading}
                  required
                />
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="password" required>
                    Password
                  </Label>
                  <Link to="/forgot-password" className="text-xs text-primary hover:underline">
                    Forgot password?
                  </Link>
                </div>
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                  required
                />
              </div>

              <Button type="submit" className="w-full" loading={loading} size="lg">
                Sign In
              </Button>

              <p className="text-center text-sm text-muted">
                Don&apos;t have an account?{" "}
                <Link to="/signup" className="text-primary hover:underline font-medium">
                  Sign up
                </Link>
              </p>
            </form>

            {/* Demo credentials hint */}
            <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200 text-xs text-blue-800">
              <p className="font-medium mb-1">Demo Credentials:</p>
              <p>Email: admin@example.com</p>
              <p>Password: password</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
