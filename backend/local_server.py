from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import sys
import os
import time

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_layer import FileRepository, InMemoryRepository
from logic_layer import LinkBusinessService, AnalyticsService

app = Flask(__name__)
CORS(app)

# Initialize services with dependency injection
repository = FileRepository('/app/data/linkpulse_data.json')  # Use InMemoryRepository() for testing
link_service = LinkBusinessService(repository)
analytics_service = AnalyticsService(repository)

@app.route('/dev/shorten', methods=['POST'])
def shorten_link():
    try:
        data = request.get_json()
        url = data.get('url')
        ttl_hours = data.get('ttl_hours', 24)
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Use business service
        link_data = link_service.create_short_link(url, ttl_hours)
        
        return jsonify({
            'slug': link_data.slug,
            'short_url': f'http://localhost:5000/u/{link_data.slug}',
            'original_url': link_data.original_url,
            'expires_at': link_data.expires_at
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/u/<slug>')
def redirect_link(slug):
    try:
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        # Use business service
        redirect_url = link_service.get_redirect_url(slug, ip, user_agent)
        
        if not redirect_url:
            return jsonify({'error': 'Link not found or expired'}), 404
        
        return redirect(redirect_url)
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/dev/analytics/<slug>')
def get_analytics(slug):
    try:
        # Use business service
        analytics = link_service.get_link_analytics(slug)
        
        if not analytics:
            return jsonify({'error': 'Link not found'}), 404
        
        return jsonify({
            'total_clicks': analytics.total_clicks,
            'first_click': analytics.first_click,
            'last_click': analytics.last_click,
            'click_logs': [
                {
                    'timestamp': log.timestamp,
                    'ip': log.ip,
                    'user_agent': log.user_agent,
                    'country': log.country
                } for log in analytics.click_logs
            ]
        })
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/dev/stats/<slug>')
def get_stats(slug):
    try:
        stats = analytics_service.get_link_stats(slug)
        if not stats:
            return jsonify({'error': 'Link not found'}), 404
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/dev/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': int(time.time())})

if __name__ == '__main__':
    print("LinkPulse Backend Server Starting...")
    print("API Base: http://localhost:5000/dev")
    print("Health Check: http://localhost:5000/dev/health")
    app.run(debug=True, port=5000)