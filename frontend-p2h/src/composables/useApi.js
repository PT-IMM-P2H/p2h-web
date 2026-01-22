/**
 * API Composable
 * Reusable logic for API calls with error handling
 */

import { ref } from 'vue'
import { api } from '../services/api'
import { API_STATUS, ERROR_MESSAGES } from '../constants'

export function useApi() {
  const loading = ref(false)
  const error = ref(null)

  /**
   * Generic API call wrapper
   * @param {Function} apiCall - API function to execute
   * @param {Object} options - Options
   * @returns {Promise} - Response data or null
   */
  const execute = async (apiCall, options = {}) => {
    const {
      showError = true,
      onSuccess = null,
      onError = null,
      loadingState = true
    } = options

    if (loadingState) loading.value = true
    error.value = null

    try {
      const response = await apiCall()
      
      // Check if response follows standard format
      if (response.data && response.data.status === API_STATUS.SUCCESS) {
        if (onSuccess) onSuccess(response.data.payload)
        return response.data.payload
      } else {
        throw new Error(response.data?.message || ERROR_MESSAGES.INTERNAL_ERROR)
      }
    } catch (err) {
      const errorMessage = err.response?.data?.message || 
                          err.message || 
                          ERROR_MESSAGES.NETWORK_ERROR
      
      error.value = errorMessage
      
      if (showError) {
        console.error('API Error:', errorMessage)
      }
      
      if (onError) onError(err)
      
      return null
    } finally {
      if (loadingState) loading.value = false
    }
  }

  /**
   * GET request
   */
  const get = async (url, params = {}, options = {}) => {
    return execute(() => api.get(url, { params }), options)
  }

  /**
   * POST request
   */
  const post = async (url, data = {}, options = {}) => {
    return execute(() => api.post(url, data), options)
  }

  /**
   * PUT request
   */
  const put = async (url, data = {}, options = {}) => {
    return execute(() => api.put(url, data), options)
  }

  /**
   * DELETE request
   */
  const del = async (url, options = {}) => {
    return execute(() => api.delete(url), options)
  }

  /**
   * PATCH request
   */
  const patch = async (url, data = {}, options = {}) => {
    return execute(() => api.patch(url, data), options)
  }

  return {
    loading,
    error,
    execute,
    get,
    post,
    put,
    delete: del,
    patch
  }
}
