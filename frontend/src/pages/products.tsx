import { useState } from "react"
import { Search, Download, Plus, MoreHorizontal } from "lucide-react"
import { MainLayout } from "@/components/layouts/main-layout"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { useProducts } from "@/services/api/hooks"
import { formatCurrency } from "@/lib/utils"

export function ProductsPage() {
  const [search, setSearch] = useState("")
  const products = useProducts()

  const filteredProducts = products.data?.filter((p) =>
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    p.sku.toLowerCase().includes(search.toLowerCase())
  ) || []

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-foreground">Products</h1>
          <p className="text-muted mt-2">Manage your product catalog</p>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-3 sm:items-center justify-between">
          <div className="flex-1 max-w-md">
            <Input
              placeholder="Search products..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              icon={<Search className="h-4 w-4" />}
            />
          </div>
          <div className="flex gap-2">
            <Button variant="secondary" size="md">
              <Download className="h-4 w-4" />
              Export
            </Button>
            <Button size="md">
              <Plus className="h-4 w-4" />
              New Product
            </Button>
          </div>
        </div>

        {/* Table */}
        <Card>
          <CardHeader>
            <CardTitle>Product Catalog</CardTitle>
            <CardDescription>All products in your inventory system</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>SKU</TableHead>
                  <TableHead>Product Name</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead>Supplier</TableHead>
                  <TableHead className="text-right">Stock</TableHead>
                  <TableHead className="text-right">Unit Price</TableHead>
                  <TableHead className="text-right">Total Value</TableHead>
                  <TableHead className="w-12"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredProducts.map((product) => {
                  const totalValue = product.currentStock * product.price

                  return (
                    <TableRow key={product.id}>
                      <TableCell className="font-mono text-sm">{product.sku}</TableCell>
                      <TableCell className="font-medium">{product.name}</TableCell>
                      <TableCell className="text-sm text-muted">{product.category}</TableCell>
                      <TableCell className="text-sm text-muted">{product.supplier}</TableCell>
                      <TableCell className="text-right">
                        <Badge variant={product.currentStock <= product.minStock ? "error" : "default"}>
                          {product.currentStock}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right">{formatCurrency(product.price)}</TableCell>
                      <TableCell className="text-right font-medium">{formatCurrency(totalValue)}</TableCell>
                      <TableCell>
                        <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
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
