import React, { createContext, useContext, useState, useEffect, useCallback } from "react"
import { apiClient, tokenStorage, ApiError } from "@/lib/api-client"
import type { User, AuthState } from "@/types"

interface LoginResponse {
  access: string
  refresh: string
  user: User
}

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  /**
   * The backend has no public self-registration endpoint (accounts are
   * created by an admin and activated via invitation), so this always
   * rejects. Kept so the signup UI can surface a clear message instead
   * of silently faking an account.
   */
  register: (email: string, password: string, firstName: string, lastName: string) => Promise<void>
  updateUser: (user: User) => void
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    loading: true,
  })

  const loadCurrentUser = useCallback(async () => {
    if (!tokenStorage.getAccess()) {
      setState({ isAuthenticated: false, user: null, loading: false })
      return
    }
    try {
      const user = await apiClient.get<User>("/auth/me/")
      setState({ isAuthenticated: true, user, loading: false })
    } catch (error) {
      tokenStorage.clear()
      setState({ isAuthenticated: false, user: null, loading: false })
    }
  }, [])

  // On mount, if we have a stored access token, validate it against the
  // backend and load the current user's profile.
  useEffect(() => {
    loadCurrentUser()
  }, [loadCurrentUser])

  const login = async (email: string, password: string) => {
    setState((prev) => ({ ...prev, loading: true }))
    try {
      const data = await apiClient.post<LoginResponse>(
        "/auth/login/",
        { email, password },
        { skipAuth: true }
      )
      tokenStorage.setTokens(data.access, data.refresh)
      setState({ isAuthenticated: true, user: data.user, loading: false })
    } catch (error) {
      setState({ isAuthenticated: false, user: null, loading: false })
      if (error instanceof ApiError) throw error
      throw new Error("Login failed")
    }
  }

  const logout = async () => {
    const refresh = tokenStorage.getRefresh()
    try {
      if (refresh) {
        await apiClient.post("/auth/logout/", { refresh })
      }
    } catch (error) {
      // Even if the backend call fails (token already expired, network
      // issue, etc.), we still want to clear local state.
    } finally {
      tokenStorage.clear()
      setState({ isAuthenticated: false, user: null, loading: false })
    }
  }

  const register = async () => {
    throw new Error(
      "Self-registration is not available. Accounts are created by an administrator and activated by invitation."
    )
  }

  const updateUser = (user: User) => {
    setState((prev) => ({ ...prev, isAuthenticated: true, user }))
  }

  return (
    <AuthContext.Provider value={{ ...state, login, logout, register, updateUser, refreshUser: loadCurrentUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
