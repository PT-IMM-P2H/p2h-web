/**
 * Composable for managing user profile data
 * Centralized user profile state and fetch logic
 */
import { ref } from 'vue'
import { api } from '../services/api'

const userProfile = ref(null)
const isLoading = ref(false)
const error = ref(null)

export function useUserProfile() {
  const fetchUserProfile = async () => {
    if (userProfile.value) {
      // Already fetched, return cached data
      return userProfile.value
    }

    isLoading.value = true
    error.value = null

    try {
      const response = await api.get('/auth/me')
      
      if (response.data.status === 'success') {
        userProfile.value = response.data.payload
        return userProfile.value
      } else {
        throw new Error(response.data.message || 'Failed to fetch user profile')
      }
    } catch (err) {
      console.error('Error fetching user profile:', err)
      error.value = err.response?.data?.message || err.message || 'Failed to load profile'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const refreshProfile = async () => {
    // Force refresh by clearing cache
    userProfile.value = null
    return fetchUserProfile()
  }

  const clearProfile = () => {
    userProfile.value = null
    error.value = null
  }

  const getUserRole = () => {
    if (!userProfile.value) return 'user'
    return userProfile.value.role
  }

  const getUserRoleLabel = () => {
    const roleMap = {
      'superadmin': 'Super Administrator',
      'admin': 'Administrator',
      'user': 'User'
    }
    return roleMap[getUserRole()] || 'User'
  }

  const getUserFullName = () => {
    if (!userProfile.value) return 'Loading...'
    return userProfile.value.full_name
  }

  return {
    userProfile,
    isLoading,
    error,
    fetchUserProfile,
    refreshProfile,
    clearProfile,
    getUserRole,
    getUserRoleLabel,
    getUserFullName
  }
}
