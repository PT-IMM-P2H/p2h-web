/**
 * Chart Composable
 * Reusable logic for Chart.js initialization and management
 */

import { ref, onUnmounted } from 'vue'
import Chart from 'chart.js/auto'

export function useChart() {
  const chartInstances = ref({})

  /**
   * Initialize a chart
   * @param {string} canvasId - Canvas element ID
   * @param {Object} config - Chart.js configuration
   * @returns {Object} - Chart instance
   */
  const initChart = (canvasId, config) => {
    // Destroy existing chart if exists
    destroyChart(canvasId)

    const canvas = document.getElementById(canvasId)
    if (!canvas) {
      console.error(`Canvas element with ID "${canvasId}" not found`)
      return null
    }

    try {
      const chart = new Chart(canvas, config)
      chartInstances.value[canvasId] = chart
      return chart
    } catch (error) {
      console.error(`Error creating chart "${canvasId}":`, error)
      return null
    }
  }

  /**
   * Update chart data
   * @param {string} canvasId - Canvas element ID
   * @param {Object} newData - New chart data
   * @param {Object} newOptions - New chart options (optional)
   */
  const updateChart = (canvasId, newData, newOptions = null) => {
    const chart = chartInstances.value[canvasId]
    if (!chart) {
      console.warn(`Chart "${canvasId}" not found`)
      return
    }

    chart.data = newData
    if (newOptions) {
      chart.options = newOptions
    }
    chart.update()
  }

  /**
   * Destroy a specific chart
   * @param {string} canvasId - Canvas element ID
   */
  const destroyChart = (canvasId) => {
    const chart = chartInstances.value[canvasId]
    if (chart) {
      chart.destroy()
      delete chartInstances.value[canvasId]
    }
  }

  /**
   * Destroy all charts
   */
  const destroyAllCharts = () => {
    Object.keys(chartInstances.value).forEach(canvasId => {
      destroyChart(canvasId)
    })
  }

  /**
   * Get chart instance
   * @param {string} canvasId - Canvas element ID
   * @returns {Object} - Chart instance
   */
  const getChart = (canvasId) => {
    return chartInstances.value[canvasId]
  }

  // Cleanup on unmount
  onUnmounted(() => {
    destroyAllCharts()
  })

  return {
    initChart,
    updateChart,
    destroyChart,
    destroyAllCharts,
    getChart
  }
}
