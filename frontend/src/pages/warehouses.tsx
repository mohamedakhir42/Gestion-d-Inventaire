import { MainLayout } from "@/components/layouts/main-layout"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { useWarehouses } from "@/services/api/hooks"
import { useState } from "react"
import { Search, Plus, MapPin, Package } from "lucide-react"

export function WarehousesPage() {
  const { data: warehouses } = useWarehouses()
  const [searchTerm, setSearchTerm] = useState("")

  const filtered = warehouses?.filter(w =>
    w.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    w.location.toLowerCase().includes(searchTerm.toLowerCase())
  ) || []

  return (
    <MainLayout>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Warehouses</h1>
            <p className="text-muted-foreground mt-2">Manage distribution centers and storage locations</p>
          </div>
          <Button size="lg">
            <Plus className="mr-2 h-4 w-4" />
            Add Warehouse
          </Button>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {filtered.map(warehouse => (
            <Card key={warehouse.id}>
              <CardContent className="pt-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="bg-blue-100 p-2 rounded-lg">
                    <MapPin className="h-5 w-5 text-blue-600" />
                  </div>
                  <Badge variant={warehouse.status === 'active' ? 'default' : 'secondary'}>
                    {warehouse.status}
                  </Badge>
                </div>
                <h3 className="font-semibold">{warehouse.name}</h3>
                <p className="text-sm text-muted-foreground">{warehouse.location}</p>
                <div className="mt-4 pt-4 border-t space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Capacity</span>
                    <span className="font-medium">{warehouse.capacity} units</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-muted-foreground">Utilization</span>
                    <span className="font-medium">{warehouse.utilization}%</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Warehouse Details</CardTitle>
              <div className="relative w-64">
                <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search warehouses..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-8"
                />
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Location</TableHead>
                  <TableHead>Capacity</TableHead>
                  <TableHead>Used</TableHead>
                  <TableHead>Available</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Manager</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filtered.map(warehouse => (
                  <TableRow key={warehouse.id}>
                    <TableCell className="font-medium">{warehouse.name}</TableCell>
                    <TableCell>{warehouse.location}</TableCell>
                    <TableCell>{warehouse.capacity}</TableCell>
                    <TableCell>{Math.round(warehouse.capacity * warehouse.utilization / 100)}</TableCell>
                    <TableCell>{Math.round(warehouse.capacity * (100 - warehouse.utilization) / 100)}</TableCell>
                    <TableCell>
                      <Badge variant={warehouse.status === 'active' ? 'default' : 'secondary'}>
                        {warehouse.status}
                      </Badge>
                    </TableCell>
                    <TableCell>{warehouse.manager}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
