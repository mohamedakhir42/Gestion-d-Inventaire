import { useState, useCallback, useEffect } from "react"
import {
  mockProducts,
  mockWarehouses,
  mockCategories,
  mockSuppliers,
  mockEmployees,
  mockStockMovements,
  mockAuditLogs,
  mockNotifications,
  mockDashboardStats,
  mockStockRequests,
  mockInventoryItems,
} from "./mock-data"
import type {
  Product,
  Warehouse,
  Category,
  Supplier,
  Employee,
  StockMovement,
  AuditLog,
  Notification,
  DashboardStats,
  StockRequest,
  InventoryItem,
} from "@/types"

interface UseQueryState<T> {
  data: T | null
  loading: boolean
  error: Error | null
}

// Generic hook for data fetching
function useQuery<T>(initialData: T) {
  const [state, setState] = useState<UseQueryState<T>>({
    data: initialData,
    loading: false,
    error: null,
  })

  return state
}

export function useProducts() {
  return useQuery(mockProducts)
}

export function useProduct(id: string) {
  const products = useQuery(mockProducts)
  return {
    ...products,
    data: products.data?.find((p) => p.id === id) || null,
  }
}

export function useWarehouses() {
  return useQuery(mockWarehouses)
}

export function useWarehouse(id: string) {
  const warehouses = useQuery(mockWarehouses)
  return {
    ...warehouses,
    data: warehouses.data?.find((w) => w.id === id) || null,
  }
}

export function useCategories() {
  return useQuery(mockCategories)
}

export function useSuppliers() {
  return useQuery(mockSuppliers)
}

export function useEmployees() {
  return useQuery(mockEmployees)
}

export function useStockMovements() {
  return useQuery(mockStockMovements)
}

export function useAuditLogs() {
  return useQuery(mockAuditLogs)
}

export function useNotifications() {
  return useQuery(mockNotifications)
}

export function useDashboardStats() {
  return useQuery(mockDashboardStats)
}

export function useStockRequests() {
  return useQuery(mockStockRequests)
}

export function useInventoryItems() {
  return useQuery(mockInventoryItems)
}

// Hook for searching products
export function useSearchProducts(query: string) {
  const products = useQuery(mockProducts)
  const filtered = products.data?.filter(
    (p) =>
      p.name.toLowerCase().includes(query.toLowerCase()) ||
      p.sku.toLowerCase().includes(query.toLowerCase()) ||
      p.barcode.toLowerCase().includes(query.toLowerCase())
  )

  return {
    ...products,
    data: filtered,
  }
}

// Hook for filtering inventory by warehouse
export function useWarehouseInventory(warehouseId: string) {
  const inventory = useQuery(mockInventoryItems)
  const filtered = inventory.data?.filter((item) => item.warehouseId === warehouseId)

  return {
    ...inventory,
    data: filtered,
  }
}

// Hook for low stock items
export function useLowStockItems() {
  const products = useQuery(mockProducts)
  const lowStock = products.data?.filter((p) => p.currentStock <= p.minStock)

  return {
    ...products,
    data: lowStock,
  }
}

// Hook for paginated data
export function usePaginatedData<T extends { id: string }>(data: T[], pageSize: number = 25) {
  const [currentPage, setCurrentPage] = useState(1)

  const totalPages = Math.ceil(data.length / pageSize)
  const startIndex = (currentPage - 1) * pageSize
  const paginatedData = data.slice(startIndex, startIndex + pageSize)

  return {
    data: paginatedData,
    currentPage,
    totalPages,
    totalItems: data.length,
    setCurrentPage,
  }
}
