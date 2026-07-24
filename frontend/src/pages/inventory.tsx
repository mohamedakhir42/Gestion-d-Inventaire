import { useState } from "react"
import { Search, Download, Filter, Plus } from "lucide-react"
import { MainLayout } from "@/components/layouts/main-layout"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { useProducts } from "@/services/api/hooks"

export function InventoryPage() {
  const [search, setSearch] = useState("")
  const products = useProducts()

  const filteredProducts = products.data?.filter((p) =>
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    p.sku.toLowerCase().includes(search.toLowerCase())
  ) || []

  const getStockStatus = (current: number, min: number, max: number) => {
    if (current <= min) return { variant: "error" as const, label: "Critical" }
    if (current >= max) return { variant: "warning" as const, label: "Overstock" }
    return { variant: "success" as const, label: "Optimal" }
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-foreground">Inventory</h1>
          <p className="text-muted mt-2">Manage stock levels across all warehouses</p>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-3 sm:items-center justify-between">
          <div className="flex-1 max-w-md flex gap-2">
            <Input
              placeholder="Search by name or SKU..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              icon={<Search className="h-4 w-4" />}
            />
            <Button variant="secondary" size="md">
              <Filter className="h-4 w-4" />
            </Button>
          </div>
          <div className="flex gap-2">
            <Button variant="secondary" size="md">
              <Download className="h-4 w-4" />
              Export
            </Button>
            <Button size="md">
              <Plus className="h-4 w-4" />
              Adjust Stock
            </Button>
          </div>
        </div>

        {/* Table */}
        <Card>
          <CardHeader>
            <CardTitle>Stock Levels</CardTitle>
            <CardDescription>Current inventory across all locations</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>SKU</TableHead>
                  <TableHead>Product Name</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead className="text-right">Current</TableHead>
                  <TableHead className="text-right">Reserved</TableHead>
                  <TableHead className="text-right">Available</TableHead>
                  <TableHead className="text-right">Min/Max</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredProducts.map((product) => {
                  const status = getStockStatus(product.currentStock, product.minStock, product.maxStock)
                  const available = product.currentStock - product.reservedStock

                  return (
                    <TableRow key={product.id}>
                      <TableCell className="font-mono text-sm">{product.sku}</TableCell>
                      <TableCell className="font-medium">{product.name}</TableCell>
                      <TableCell className="text-sm text-muted">{product.category}</TableCell>
                      <TableCell className="text-right font-mono">{product.currentStock}</TableCell>
                      <TableCell className="text-right font-mono">{product.reservedStock}</TableCell>
                      <TableCell className="text-right font-mono">{available}</TableCell>
                      <TableCell className="text-right text-sm">
                        {product.minStock} / {product.maxStock}
                      </TableCell>
                      <TableCell>
                        <Badge variant={status.variant}>{status.label}</Badge>
                      </TableCell>
                    </TableRow>
                  )
                })}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
