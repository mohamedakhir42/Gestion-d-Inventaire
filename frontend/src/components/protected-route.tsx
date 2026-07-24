import { Navigate } from "react-router-dom"
import { useAuth } from "@/contexts/auth-context"
import { PageLoader } from "@/components/ui/loader"

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading } = useAuth()

  if (loading) {
    return <PageLoader />
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}
