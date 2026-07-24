import { useState } from "react"
import { Link, useLocation } from "react-router-dom"
import {
  BarChart3,
  Package,
  Boxes,
  Building2,
  Layers,
  ClipboardList,
  ArrowRightLeft,
  Users,
  Bell,
  FileText,
  BarChart,
  Menu,
  X,
  Settings,
  LogOut,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { useAuth } from "@/contexts/auth-context"

const menuItems = [
  { id: "dashboard", label: "Dashboard", path: "/dashboard", icon: BarChart3 },
  { id: "inventory", label: "Inventory", path: "/inventory", icon: Package },
  { id: "products", label: "Products", path: "/products", icon: Boxes },
  { id: "warehouses", label: "Warehouses", path: "/warehouses", icon: Building2 },
  { id: "stocks", label: "Stock Levels", path: "/stock-levels", icon: Layers },
  { id: "requests", label: "Stock Requests", path: "/stock-requests", icon: ClipboardList },
  { id: "movements", label: "Movements", path: "/movements", icon: ArrowRightLeft },
  { id: "employees", label: "Employees", path: "/employees", icon: Users },
  { id: "notifications", label: "Notifications", path: "/notifications", icon: Bell },
  { id: "audit", label: "Audit Logs", path: "/audit-logs", icon: FileText },
  { id: "reports", label: "Reports", path: "/reports", icon: BarChart },
]

export function Sidebar() {
  const [isOpen, setIsOpen] = useState(true)
  const location = useLocation()
  const { logout } = useAuth()

  const isActive = (path: string) => location.pathname === path

  return (
    <>
      {/* Mobile menu button */}
      <Button
        variant="ghost"
        size="sm"
        className="fixed top-4 left-4 z-40 lg:hidden"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
      </Button>

      {/* Sidebar backdrop */}
      {isOpen && (
        <div className="fixed inset-0 z-30 bg-black/50 lg:hidden" onClick={() => setIsOpen(false)} />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed left-0 top-0 z-40 h-screen w-64 overflow-y-auto border-r border-border bg-white transition-transform duration-300 lg:translate-x-0",
          isOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="border-b border-border p-6">
            <h1 className="text-xl font-bold text-primary">InventoryPro</h1>
            <p className="text-xs text-muted">Industrial Management</p>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 p-4">
            {menuItems.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.id}
                  to={item.path}
                  onClick={() => setIsOpen(false)}
                  className={cn(
                    "flex items-center gap-3 rounded-lg px-4 py-2.5 text-sm font-medium transition-smooth",
                    isActive(item.path)
                      ? "bg-primary text-white shadow-md"
                      : "text-foreground hover:bg-gray-100"
                  )}
                >
                  <Icon className="h-5 w-5" />
                  <span>{item.label}</span>
                </Link>
              )
            })}
          </nav>

          {/* Footer */}
          <div className="border-t border-border p-4 space-y-2">
            <Link to="/settings">
              <Button variant="ghost" size="md" className="w-full justify-start gap-3">
                <Settings className="h-5 w-5" />
                <span>Settings</span>
              </Button>
            </Link>
            <Button
              variant="ghost"
              size="md"
              className="w-full justify-start gap-3 text-error hover:text-error"
              onClick={logout}
            >
              <LogOut className="h-5 w-5" />
              <span>Logout</span>
            </Button>
          </div>
        </div>
      </aside>

      {/* Content offset */}
      <div className="lg:pl-64" />
    </>
  )
}
