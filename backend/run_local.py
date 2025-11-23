#!/usr/bin/env python3
"""
LinkPulse Local Backend Server
Run this script to start the local development server
"""

import os
import sys
import subprocess

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements_local.txt'])

def run_server():
    """Start the Flask development server"""
    print("Starting LinkPulse Backend Server...")
    print("API will be available at: http://localhost:5000/dev")
    print("Health check: http://localhost:5000/dev/health")
    print("Test with: curl http://localhost:5000/dev/health")
    print("-" * 50)
    
    # Import and run the server
    from local_server import app
    app.run(debug=True, port=5000, host='0.0.0.0')

if __name__ == '__main__':
    try:
        # Check if requirements are installed
        try:
            import flask
            import flask_cors
            import requests
        except ImportError:
            install_requirements()
        
        run_server()
        
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)