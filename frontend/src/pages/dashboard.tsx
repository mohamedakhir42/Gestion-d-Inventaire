import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"
import { AlertCircle, TrendingUp, Package, Warehouse, Users, Clock } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { MainLayout } from "@/components/layouts/main-layout"
import { Button } from "@/components/ui/button"
import { useDashboardStats, useLowStockItems } from "@/services/api/hooks"
import { formatCurrency } from "@/lib/utils"
import { CHART_COLORS } from "@/lib/constants"

// Chart data
const stockMovementData = [
  { month: "Jan", inbound: 2400, outbound: 2210, net: 190 },
  { month: "Feb", inbound: 3001, outbound: 2290, net: 711 },
  { month: "Mar", inbound: 2000, outbound: 1690, net: 310 },
  { month: "Apr", inbound: 2780, outbound: 2001, net: 779 },
  { month: "May", inbound: 1890, outbound: 1500, net: 390 },
  { month: "Jun", inbound: 2390, outbound: 1800, net: 590 },
]

const warehouseUtilization = [
  { name: "Main Warehouse", value: 72 },
  { name: "Distribution Center", value: 70 },
  { name: "Regional Hub", value: 55 },
]

const topProducts = [
  { name: "Steel Bearing", value: 450 },
  { name: "Motor Controller", value: 380 },
  { name: "Fastener Kit", value: 320 },
  { name: "Pump Assembly", value: 280 },
  { name: "Conveyor Belt", value: 220 },
]

function StatCard({
  icon: Icon,
  label,
  value,
  change,
  changeType = "positive",
}: {
  icon: React.ElementType
  label: string
  value: string | number
  change?: string
  changeType?: "positive" | "negative"
}) {
  return (
    <Card className="hover:shadow-lg transition-smooth">
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-sm text-muted mb-1">{label}</p>
            <p className="text-2xl font-bold text-foreground mb-3">{value}</p>
            {change && (
              <p className={`text-xs font-medium ${changeType === "positive" ? "text-success" : "text-error"}`}>
                {changeType === "positive" ? "+" : ""}{change} from last month
              </p>
            )}
          </div>
          <div className="p-3 bg-primary/10 rounded-lg">
            <Icon className="h-6 w-6 text-primary" />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

function RecentActivity() {
  const activities = [
    { time: "2 hours ago", action: "Stock transfer completed", entity: "WH-001 → WH-002" },
    { time: "4 hours ago", action: "Low stock alert", entity: "PROD-004: Motor Controller" },
    { time: "6 hours ago", action: "New stock request approved", entity: "PROD-001 (100 units)" },
    { time: "1 day ago", action: "Physical inventory count", entity: "Main Warehouse" },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Clock className="h-5 w-5" />
          Recent Activity
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {activities.map((activity, i) => (
            <div key={i} className="flex gap-4">
              <div className="flex flex-col items-center">
                <div className="h-3 w-3 rounded-full bg-primary mt-1.5" />
                {i < activities.length - 1 && <div className="h-12 w-0.5 bg-border mt-1" />}
              </div>
              <div className="pb-4">
                <p className="text-sm font-medium text-foreground">{activity.action}</p>
                <p className="text-xs text-muted mt-0.5">{activity.entity}</p>
                <p className="text-xs text-muted/70 mt-1">{activity.time}</p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

export function DashboardPage() {
  const stats = useDashboardStats()
  const lowStock = useLowStockItems()

  return (
    <MainLayout>
      <div className="space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-foreground">Dashboard</h1>
          <p className="text-muted mt-2">Welcome back! Here&apos;s an overview of your inventory.</p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <StatCard
            icon={Package}
            label="Total Products"
            value={stats.data?.totalProducts || 0}
            change="12"
            changeType="positive"
          />
          <StatCard
            icon={TrendingUp}
            label="Inventory Value"
            value={formatCurrency(stats.data?.inventoryValue || 0)}
            change="8.2%"
            changeType="positive"
          />
          <StatCard
            icon={AlertCircle}
            label="Critical Stock"
            value={stats.data?.criticalStockItems || 0}
            change="2"
            changeType="negative"
          />
          <StatCard
            icon={Clock}
            label="Pending Requests"
            value={stats.data?.pendingRequests || 0}
            change="5"
            changeType="positive"
          />
          <StatCard
            icon={Users}
            label="Active Employees"
            value={stats.data?.activeEmployees || 0}
            change="3"
            changeType="positive"
          />
          <StatCard
            icon={Warehouse}
            label="Total Warehouses"
            value={stats.data?.totalWarehouses || 0}
            change="0"
          />
        </div>

        {/* Charts Row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Stock Movement Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Monthly Stock Movements</CardTitle>
              <CardDescription>Inbound vs Outbound trends</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={stockMovementData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="month" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip contentStyle={{ backgroundColor: "#fff", border: "1px solid #e5e7eb" }} />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="inbound"
                    stroke={CHART_COLORS.primary}
                    strokeWidth={2}
                    dot={{ fill: CHART_COLORS.primary }}
                  />
                  <Line
                    type="monotone"
                    dataKey="outbound"
                    stroke={CHART_COLORS.secondary}
                    strokeWidth={2}
                    dot={{ fill: CHART_COLORS.secondary }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Warehouse Utilization */}
          <Card>
            <CardHeader>
              <CardTitle>Warehouse Utilization</CardTitle>
              <CardDescription>Current capacity usage</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={warehouseUtilization}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="name" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip contentStyle={{ backgroundColor: "#fff", border: "1px solid #e5e7eb" }} />
                  <Bar dataKey="value" fill={CHART_COLORS.primary} radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Charts Row 2 */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Top Products */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle>Top Consumed Products</CardTitle>
              <CardDescription>By quantity this period</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={topProducts}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="name" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip contentStyle={{ backgroundColor: "#fff", border: "1px solid #e5e7eb" }} />
                  <Bar dataKey="value" fill={CHART_COLORS.accent} radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Low Stock Alert */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-error">
                <AlertCircle className="h-5 w-5" />
                Low Stock Alert
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {lowStock.data?.slice(0, 5).map((product) => (
                  <div key={product.id} className="p-3 bg-red-50 rounded-lg border border-red-200">
                    <p className="text-sm font-medium text-foreground">{product.name}</p>
                    <div className="flex items-center justify-between mt-2">
                      <span className="text-xs text-muted">Current: {product.currentStock}</span>
                      <span className="text-xs text-error font-medium">Min: {product.minStock}</span>
                    </div>
                    <Button size="sm" className="w-full mt-2">
                      Reorder
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Activity */}
        <RecentActivity />
      </div>
    </MainLayout>
  )
}
