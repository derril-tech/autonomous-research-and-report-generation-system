'use client'

import React, { createContext, useContext, useReducer, useEffect } from 'react'
import { authApi } from '@/lib/api/auth'

interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  organization?: string
  role: string
  is_active: boolean
  created_at: string
  last_login?: string
  preferences?: {
    default_format: string
    notification_email: boolean
    auto_save: boolean
  }
}

interface AuthState {
  user: User | null
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

type AuthAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: { user: User; token: string; refreshToken: string } }
  | { type: 'LOGIN_FAILURE'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'REFRESH_TOKEN'; payload: { token: string; refreshToken: string } }
  | { type: 'UPDATE_USER'; payload: User }
  | { type: 'CLEAR_ERROR' }

const initialState: AuthState = {
  user: null,
  token: null,
  refreshToken: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
}

function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'LOGIN_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      }
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        refreshToken: action.payload.refreshToken,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      }
    case 'LOGIN_FAILURE':
      return {
        ...state,
        user: null,
        token: null,
        refreshToken: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload,
      }
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        token: null,
        refreshToken: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      }
    case 'REFRESH_TOKEN':
      return {
        ...state,
        token: action.payload.token,
        refreshToken: action.payload.refreshToken,
      }
    case 'UPDATE_USER':
      return {
        ...state,
        user: action.payload,
      }
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      }
    default:
      return state
  }
}

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>
  register: (userData: RegisterData) => Promise<void>
  logout: () => Promise<void>
  refreshToken: () => Promise<void>
  updateUser: (userData: Partial<User>) => Promise<void>
  clearError: () => void
}

interface RegisterData {
  email: string
  password: string
  first_name: string
  last_name: string
  organization?: string
  role?: string
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, initialState)

  // Initialize auth state from localStorage
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const token = localStorage.getItem('token')
        const refreshToken = localStorage.getItem('refreshToken')
        const userData = localStorage.getItem('user')

        if (token && refreshToken && userData) {
          const user = JSON.parse(userData)
          dispatch({
            type: 'LOGIN_SUCCESS',
            payload: { user, token, refreshToken },
          })
        } else {
          dispatch({ type: 'LOGOUT' })
        }
      } catch (error) {
        console.error('Failed to initialize auth:', error)
        dispatch({ type: 'LOGOUT' })
      }
    }

    initializeAuth()
  }, [])

  // Auto-refresh token
  useEffect(() => {
    if (!state.token || !state.refreshToken) return

    const refreshInterval = setInterval(async () => {
      try {
        await refreshToken()
      } catch (error) {
        console.error('Failed to refresh token:', error)
        await logout()
      }
    }, 14 * 60 * 1000) // Refresh every 14 minutes

    return () => clearInterval(refreshInterval)
  }, [state.token, state.refreshToken])

  const login = async (email: string, password: string) => {
    try {
      dispatch({ type: 'LOGIN_START' })
      const response = await authApi.login({ email, password })
      
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('refreshToken', response.refresh_token)
      localStorage.setItem('user', JSON.stringify(response.user))
      
      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: {
          user: response.user,
          token: response.access_token,
          refreshToken: response.refresh_token,
        },
      })
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 'Login failed'
      dispatch({ type: 'LOGIN_FAILURE', payload: errorMessage })
      throw error
    }
  }

  const register = async (userData: RegisterData) => {
    try {
      dispatch({ type: 'LOGIN_START' })
      const response = await authApi.register(userData)
      
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('refreshToken', response.refresh_token)
      localStorage.setItem('user', JSON.stringify(response.user))
      
      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: {
          user: response.user,
          token: response.access_token,
          refreshToken: response.refresh_token,
        },
      })
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 'Registration failed'
      dispatch({ type: 'LOGIN_FAILURE', payload: errorMessage })
      throw error
    }
  }

  const logout = async () => {
    try {
      if (state.token) {
        await authApi.logout()
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('user')
      dispatch({ type: 'LOGOUT' })
    }
  }

  const refreshToken = async () => {
    try {
      if (!state.refreshToken) throw new Error('No refresh token')
      
      const response = await authApi.refresh({ refresh_token: state.refreshToken })
      
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('refreshToken', response.refresh_token)
      
      dispatch({
        type: 'REFRESH_TOKEN',
        payload: {
          token: response.access_token,
          refreshToken: response.refresh_token,
        },
      })
    } catch (error) {
      throw error
    }
  }

  const updateUser = async (userData: Partial<User>) => {
    try {
      const updatedUser = await authApi.updateProfile(userData)
      localStorage.setItem('user', JSON.stringify(updatedUser))
      dispatch({ type: 'UPDATE_USER', payload: updatedUser })
    } catch (error) {
      throw error
    }
  }

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' })
  }

  const value: AuthContextType = {
    ...state,
    login,
    register,
    logout,
    refreshToken,
    updateUser,
    clearError,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
