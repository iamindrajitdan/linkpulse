import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:5000/dev'
const DEMO_MODE = false // Set to true for demo mode

function Analytics({ slug }) {
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (slug) {
      fetchAnalytics()
    }
  }, [slug])

  const generateMockAnalytics = () => {
    const now = Math.floor(Date.now() / 1000)
    return {
      total_clicks: Math.floor(Math.random() * 50) + 1,
      first_click: now - 3600,
      last_click: now - 300,
      click_logs: [
        { timestamp: now - 300, ip: '192.168.1.1', country: 'US', user_agent: 'Chrome' },
        { timestamp: now - 1800, ip: '10.0.0.1', country: 'CA', user_agent: 'Firefox' },
        { timestamp: now - 3600, ip: '172.16.0.1', country: 'UK', user_agent: 'Safari' }
      ]
    }
  }

  const fetchAnalytics = async () => {
    setLoading(true)
    try {
      if (DEMO_MODE) {
        await new Promise(resolve => setTimeout(resolve, 500))
        setAnalytics(generateMockAnalytics())
      } else {
        const response = await axios.get(`${API_BASE}/analytics/${slug}`)
        setAnalytics(response.data)
      }
    } catch (err) {
      console.error('Failed to fetch analytics:', err)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleString()
  }

  if (loading) {
    return <div className="text-center py-4">Loading analytics...</div>
  }

  if (!analytics) {
    return null
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-semibold">Analytics</h2>
        <button
          onClick={fetchAnalytics}
          className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200"
        >
          Refresh
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-blue-800">Total Clicks</h3>
          <p className="text-3xl font-bold text-blue-600">{analytics.total_clicks}</p>
        </div>
        
        <div className="bg-green-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-green-800">First Click</h3>
          <p className="text-sm text-green-600">
            {analytics.first_click ? formatDate(analytics.first_click) : 'No clicks yet'}
          </p>
        </div>
        
        <div className="bg-purple-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold text-purple-800">Last Click</h3>
          <p className="text-sm text-purple-600">
            {analytics.last_click ? formatDate(analytics.last_click) : 'No clicks yet'}
          </p>
        </div>
      </div>
      
      {analytics.click_logs.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold mb-3">Recent Clicks</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Time</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Country</th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">IP</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {analytics.click_logs.slice(-10).reverse().map((log, index) => (
                  <tr key={index}>
                    <td className="px-4 py-2 text-sm text-gray-900">{formatDate(log.timestamp)}</td>
                    <td className="px-4 py-2 text-sm text-gray-900">{log.country}</td>
                    <td className="px-4 py-2 text-sm text-gray-900">{log.ip}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default Analytics