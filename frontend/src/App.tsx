import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import { Toaster } from "sonner"
import { AuthProvider } from "@/contexts/auth-context"
import { ProtectedRoute } from "@/components/protected-route"
import { LoginPage } from "@/pages/auth/login"
import { DashboardPage } from "@/pages/dashboard"
import { InventoryPage } from "@/pages/inventory"
import { ProductsPage } from "@/pages/products"
import { WarehousesPage } from "@/pages/warehouses"
import { StockLevelsPage } from "@/pages/stock-levels"
import { EmployeesPage } from "@/pages/employees"

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          {/* Auth Routes */}
          <Route path="/login" element={<LoginPage />} />

          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/inventory"
            element={
              <ProtectedRoute>
                <InventoryPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/products"
            element={
              <ProtectedRoute>
                <ProductsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/warehouses"
            element={
              <ProtectedRoute>
                <WarehousesPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/stock-levels"
            element={
              <ProtectedRoute>
                <StockLevelsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/employees"
            element={
              <ProtectedRoute>
                <EmployeesPage />
              </ProtectedRoute>
            }
          />

          {/* Redirect */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
        <Toaster />
      </AuthProvider>
    </Router>
  )
}

export default App
