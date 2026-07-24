// Central HTTP client for talking to the Django REST backend.
// Handles the base URL, JSON encoding, JWT auth headers, and
// transparent access-token refresh on 401 responses.

const API_BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) || "http://localhost:8000/api"

const ACCESS_TOKEN_KEY = "inventorypro_access_token"
const REFRESH_TOKEN_KEY = "inventorypro_refresh_token"

export const tokenStorage = {
  getAccess: () => localStorage.getItem(ACCESS_TOKEN_KEY),
  getRefresh: () => localStorage.getItem(REFRESH_TOKEN_KEY),
  setTokens: (access: string, refresh: string) => {
    localStorage.setItem(ACCESS_TOKEN_KEY, access)
    localStorage.setItem(REFRESH_TOKEN_KEY, refresh)
  },
  setAccess: (access: string) => localStorage.setItem(ACCESS_TOKEN_KEY, access),
  clear: () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
  },
}

export class ApiError extends Error {
  status: number
  body: unknown

  constructor(status: number, message: string, body?: unknown) {
    super(message)
    this.name = "ApiError"
    this.status = status
    this.body = body
  }
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

type QueryParams = Record<string, string | number | boolean | undefined | null>

interface RequestOptions {
  method?: "GET" | "POST" | "PATCH" | "PUT" | "DELETE"
  body?: unknown
  params?: QueryParams
  /** Skip attaching the Authorization header (login, token refresh, etc). */
  skipAuth?: boolean
}

function buildUrl(path: string, params?: QueryParams): string {
  const url = new URL(`${API_BASE_URL}${path}`)
  if (params) {
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined && value !== null && value !== "") {
        url.searchParams.set(key, String(value))
      }
    }
  }
  return url.toString()
}

// Ensures concurrent 401s only trigger a single refresh request.
let refreshInFlight: Promise<string | null> | null = null

async function refreshAccessToken(): Promise<string | null> {
  const refresh = tokenStorage.getRefresh()
  if (!refresh) return null

  if (!refreshInFlight) {
    refreshInFlight = fetch(buildUrl("/auth/token/refresh/"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh }),
    })
      .then(async (res) => {
        if (!res.ok) {
          tokenStorage.clear()
          return null
        }
        const data = (await res.json()) as { access: string }
        tokenStorage.setAccess(data.access)
        return data.access
      })
      .catch(() => {
        tokenStorage.clear()
        return null
      })
      .finally(() => {
        refreshInFlight = null
      })
  }

  return refreshInFlight
}

async function parseErrorBody(res: Response): Promise<unknown> {
  try {
    return await res.json()
  } catch {
    return null
  }
}

function extractMessage(body: unknown, fallback: string): string {
  if (body && typeof body === "object") {
    const record = body as Record<string, unknown>
    if (typeof record.detail === "string") return record.detail
    const firstKey = Object.keys(record)[0]
    if (firstKey) {
      const value = record[firstKey]
      if (Array.isArray(value) && typeof value[0] === "string") return value[0]
      if (typeof value === "string") return value
    }
  }
  return fallback
}

async function request<T>(path: string, options: RequestOptions = {}, isRetry = false): Promise<T> {
  const { method = "GET", body, params, skipAuth } = options

  const headers: Record<string, string> = { "Content-Type": "application/json" }
  const access = tokenStorage.getAccess()
  if (access && !skipAuth) {
    headers.Authorization = `Bearer ${access}`
  }

  const res = await fetch(buildUrl(path, params), {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })

  if (res.status === 401 && !skipAuth && !isRetry) {
    const newAccess = await refreshAccessToken()
    if (newAccess) {
      return request<T>(path, options, true)
    }
    tokenStorage.clear()
    if (typeof window !== "undefined" && window.location.pathname !== "/login") {
      window.location.href = "/login"
    }
    throw new ApiError(401, "Session expired")
  }

  if (!res.ok) {
    const errBody = await parseErrorBody(res)
    throw new ApiError(res.status, extractMessage(errBody, res.statusText), errBody)
  }

  if (res.status === 204) {
    return undefined as T
  }

  return (await res.json()) as T
}

export const apiClient = {
  get: <T>(path: string, params?: QueryParams, options?: Pick<RequestOptions, "skipAuth">) =>
    request<T>(path, { method: "GET", params, ...options }),
  post: <T>(path: string, body?: unknown, options?: Pick<RequestOptions, "skipAuth" | "params">) =>
    request<T>(path, { method: "POST", body, ...options }),
  patch: <T>(path: string, body?: unknown) => request<T>(path, { method: "PATCH", body }),
  put: <T>(path: string, body?: unknown) => request<T>(path, { method: "PUT", body }),
  delete: <T>(path: string) => request<T>(path, { method: "DELETE" }),
}
