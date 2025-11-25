import React, { useState } from 'react'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/dev'
const DEMO_MODE = false // Set to true for demo mode

function LinkShortener({ onLinkCreated }) {
  const [url, setUrl] = useState('')
  const [ttlHours, setTtlHours] = useState(24)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const generateSlug = () => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return Array.from({length: 7}, () => chars[Math.floor(Math.random() * chars.length)]).join('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    // Validate Google Drive URL
    if (!url.includes('drive.google.com') && !url.includes('docs.google.com')) {
      setError('Only Google Drive URLs are allowed')
      setLoading(false)
      return
    }
    
    try {
      if (DEMO_MODE) {
        // Mock response for demo
        await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API delay
        const slug = generateSlug()
        const mockResult = {
          slug,
          short_url: `https://linkpulse.app/u/${slug}`,
          original_url: url,
          expires_at: Math.floor(Date.now() / 1000) + (ttlHours * 3600)
        }
        setResult(mockResult)
        onLinkCreated(slug)
        setUrl('')
      } else {
        const response = await axios.post(`${API_BASE}/shorten`, {
          url,
          ttl_hours: ttlHours
        })
        setResult(response.data)
        onLinkCreated(response.data.slug)
        setUrl('')
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to shorten link')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-2xl font-semibold mb-4">Shorten Your Google Drive Link</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Paste your Google Drive link here..."
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
        </div>
        
        <div className="flex items-center space-x-4">
          <label className="text-sm text-gray-600">Expires in:</label>
          <select
            value={ttlHours}
            onChange={(e) => setTtlHours(Number(e.target.value))}
            className="px-3 py-1 border border-gray-300 rounded-md"
          >
            <option value={1}>1 hour</option>
            <option value={24}>24 hours</option>
            <option value={168}>7 days</option>
            <option value={720}>30 days</option>
          </select>
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Shortening...' : 'Shorten Link'}
        </button>
      </form>
      
      {error && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}
      
      {result && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded">
          <h3 className="font-semibold text-green-800 mb-2">Link shortened successfully!</h3>
          <div className="space-y-2">
            <div>
              <span className="text-sm text-gray-600">Short URL: </span>
              <a href={result.short_url} className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">
                {result.short_url}
              </a>
            </div>
            <div>
              <span className="text-sm text-gray-600">Slug: </span>
              <code className="bg-gray-100 px-2 py-1 rounded">{result.slug}</code>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default LinkShortener