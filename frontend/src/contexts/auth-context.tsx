import React, { createContext, useContext, useState, useEffect } from "react"
import type { User, AuthState } from "@/types"

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  register: (email: string, password: string, firstName: string, lastName: string) => Promise<void>
  updateUser: (user: User) => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    loading: true,
  })

  // Check if user is logged in on mount
  useEffect(() => {
    const storedUser = localStorage.getItem("user")
    if (storedUser) {
      try {
        setState({
          isAuthenticated: true,
          user: JSON.parse(storedUser),
          loading: false,
        })
      } catch (error) {
        console.error("Failed to parse stored user", error)
        setState({ isAuthenticated: false, user: null, loading: false })
      }
    } else {
      setState({ isAuthenticated: false, user: null, loading: false })
    }
  }, [])

  const login = async (email: string, password: string) => {
    setState((prev) => ({ ...prev, loading: true }))
    try {
      // Mock API call - replace with real API
      const mockUser: User = {
        id: "1",
        email,
        firstName: "Admin",
        lastName: "User",
        role: "admin",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      }
      localStorage.setItem("user", JSON.stringify(mockUser))
      setState({
        isAuthenticated: true,
        user: mockUser,
        loading: false,
      })
    } catch (error) {
      console.error("Login failed", error)
      setState({ isAuthenticated: false, user: null, loading: false })
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem("user")
    setState({
      isAuthenticated: false,
      user: null,
      loading: false,
    })
  }

  const register = async (email: string, password: string, firstName: string, lastName: string) => {
    setState((prev) => ({ ...prev, loading: true }))
    try {
      // Mock API call - replace with real API
      const newUser: User = {
        id: Math.random().toString(),
        email,
        firstName,
        lastName,
        role: "user",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      }
      localStorage.setItem("user", JSON.stringify(newUser))
      setState({
        isAuthenticated: true,
        user: newUser,
        loading: false,
      })
    } catch (error) {
      console.error("Registration failed", error)
      setState({ isAuthenticated: false, user: null, loading: false })
      throw error
    }
  }

  const updateUser = (user: User) => {
    localStorage.setItem("user", JSON.stringify(user))
    setState({
      isAuthenticated: true,
      user,
      loading: false,
    })
  }

  return (
    <AuthContext.Provider value={{ ...state, login, logout, register, updateUser }}>
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
