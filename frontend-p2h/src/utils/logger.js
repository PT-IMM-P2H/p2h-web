/**
 * Logger Utility
 * Centralized logging for development and production
 */

import { DEBUG_MODE, IS_PRODUCTION } from '../config/app.config'

class Logger {
  constructor() {
    this.debugMode = DEBUG_MODE
    this.isProduction = IS_PRODUCTION
  }

  /**
   * Log info message
   */
  info(message, ...args) {
    if (!this.isProduction || this.debugMode) {
      console.log(`ℹ️ [INFO]`, message, ...args)
    }
  }

  /**
   * Log success message
   */
  success(message, ...args) {
    if (!this.isProduction || this.debugMode) {
      console.log(`✅ [SUCCESS]`, message, ...args)
    }
  }

  /**
   * Log warning message
   */
  warn(message, ...args) {
    if (!this.isProduction || this.debugMode) {
      console.warn(`⚠️ [WARNING]`, message, ...args)
    }
  }

  /**
   * Log error message
   */
  error(message, ...args) {
    console.error(`❌ [ERROR]`, message, ...args)
    
    // In production, you might want to send errors to a logging service
    if (this.isProduction) {
      this.sendToErrorTracking(message, args)
    }
  }

  /**
   * Log debug message
   */
  debug(message, ...args) {
    if (this.debugMode) {
      console.log(`🐛 [DEBUG]`, message, ...args)
    }
  }

  /**
   * Log API request
   */
  apiRequest(method, url, data = null) {
    if (this.debugMode) {
      console.log(`🌐 [API ${method.toUpperCase()}]`, url, data || '')
    }
  }

  /**
   * Log API response
   */
  apiResponse(method, url, response, duration = null) {
    if (this.debugMode) {
      const time = duration ? ` (${duration}ms)` : ''
      console.log(`📡 [API RESPONSE]`, `${method.toUpperCase()} ${url}${time}`, response)
    }
  }

  /**
   * Log API error
   */
  apiError(method, url, error) {
    console.error(`❌ [API ERROR]`, `${method.toUpperCase()} ${url}`, error)
  }

  /**
   * Send error to tracking service (e.g., Sentry)
   * @private
   */
  sendToErrorTracking(message, args) {
    // TODO: Implement error tracking service integration
    // Example: Sentry.captureException(new Error(message))
  }

  /**
   * Group logs together
   */
  group(label, callback) {
    if (!this.isProduction || this.debugMode) {
      console.group(label)
      callback()
      console.groupEnd()
    }
  }

  /**
   * Time execution of a function
   */
  time(label, callback) {
    if (!this.isProduction || this.debugMode) {
      console.time(label)
      const result = callback()
      console.timeEnd(label)
      return result
    }
    return callback()
  }
}

export const logger = new Logger()
export default logger
