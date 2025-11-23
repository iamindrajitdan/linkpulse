import React, { useState } from 'react'
import LinkShortener from './components/LinkShortener'
import Analytics from './components/Analytics'

function App() {
  const [currentSlug, setCurrentSlug] = useState('')

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-blue-600 mb-2">LinkPulse</h1>
          <p className="text-gray-600">Shorten and track your Google Drive links</p>
          <div className="mt-2 inline-block bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
            ✅ Live Backend - Full functionality enabled!
          </div>
        </header>
        
        <div className="max-w-4xl mx-auto">
          <LinkShortener onLinkCreated={setCurrentSlug} />
          {currentSlug && <Analytics slug={currentSlug} />}
        </div>
      </div>
    </div>
  )
}

export default App