/**
 * Date Utilities Composable
 * Reusable date formatting and manipulation functions
 */

import { DATE_FORMATS, MONTH_NAMES_ID, MONTH_NAMES_EN } from '../constants'

export function useDateUtils() {
  /**
   * Format date to specific format
   * @param {Date|string} date - Date to format
   * @param {string} format - Format string
   * @returns {string} - Formatted date
   */
  const formatDate = (date, format = DATE_FORMATS.DISPLAY) => {
    if (!date) return ''
    
    const d = new Date(date)
    if (isNaN(d.getTime())) return ''

    const day = String(d.getDate()).padStart(2, '0')
    const month = String(d.getMonth() + 1).padStart(2, '0')
    const year = d.getFullYear()
    const hours = String(d.getHours()).padStart(2, '0')
    const minutes = String(d.getMinutes()).padStart(2, '0')

    const formats = {
      [DATE_FORMATS.ISO]: `${year}-${month}-${day}`,
      [DATE_FORMATS.MONTH]: `${year}-${month}`,
      [DATE_FORMATS.DISPLAY]: `${day}/${month}/${year}`,
      [DATE_FORMATS.DATETIME]: `${day}/${month}/${year} ${hours}:${minutes}`
    }

    return formats[format] || formats[DATE_FORMATS.DISPLAY]
  }

  /**
   * Get month name by index
   * @param {number} monthIndex - Month index (0-11)
   * @param {string} language - Language ('id' or 'en')
   * @returns {string} - Month name
   */
  const getMonthName = (monthIndex, language = 'id') => {
    const names = language === 'id' ? MONTH_NAMES_ID : MONTH_NAMES_EN
    return names[monthIndex] || ''
  }

  /**
   * Get current date in ISO format
   * @returns {string} - Current date (YYYY-MM-DD)
   */
  const getCurrentDate = () => {
    return formatDate(new Date(), DATE_FORMATS.ISO)
  }

  /**
   * Get current month in format YYYY-MM
   * @returns {string} - Current month
   */
  const getCurrentMonth = () => {
    return formatDate(new Date(), DATE_FORMATS.MONTH)
  }

  /**
   * Add days to date
   * @param {Date|string} date - Starting date
   * @param {number} days - Number of days to add
   * @returns {Date} - New date
   */
  const addDays = (date, days) => {
    const d = new Date(date)
    d.setDate(d.getDate() + days)
    return d
  }

  /**
   * Subtract days from date
   * @param {Date|string} date - Starting date
   * @param {number} days - Number of days to subtract
   * @returns {Date} - New date
   */
  const subtractDays = (date, days) => {
    return addDays(date, -days)
  }

  /**
   * Check if date is today
   * @param {Date|string} date - Date to check
   * @returns {boolean}
   */
  const isToday = (date) => {
    const d = new Date(date)
    const today = new Date()
    return d.toDateString() === today.toDateString()
  }

  /**
   * Get date range
   * @param {Date|string} startDate
   * @param {Date|string} endDate
   * @returns {number} - Number of days between dates
   */
  const getDateDifference = (startDate, endDate) => {
    const start = new Date(startDate)
    const end = new Date(endDate)
    const diffTime = Math.abs(end - start)
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  }

  return {
    formatDate,
    getMonthName,
    getCurrentDate,
    getCurrentMonth,
    addDays,
    subtractDays,
    isToday,
    getDateDifference
  }
}
