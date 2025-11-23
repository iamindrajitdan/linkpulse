# LinkPulse 🔗

A modern, containerized URL shortener with analytics tracking. Built with React frontend and Flask backend, optimized for Docker deployment.

## ✨ Features

- **URL Shortening**: Create short links with custom TTL
- **Analytics Tracking**: Monitor clicks, IPs, user agents, and geographic data
- **Real-time Dashboard**: View link performance and statistics
- **Containerized**: Fully dockerized with optimized images
- **Persistent Storage**: Data persistence with Docker volumes
- **Health Monitoring**: Built-in health checks for both services

## 🚀 Quick Start

### Using Docker Compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/iamindrajitdan/linkpulse.git
cd linkpulse

# Build and run both services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

### Individual Services

#### Frontend
```bash
cd frontend
docker build -t linkpulse-frontend .
docker run -p 3000:3000 linkpulse-frontend
```

#### Backend
```bash
cd backend
docker build -t linkpulse-backend .
docker run -p 5000:5000 linkpulse-backend
```

## 🌐 Access URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/dev
- **Health Check**: http://localhost:5000/dev/health

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/dev/shorten` | Create short link |
| GET | `/u/<slug>` | Redirect to original URL |
| GET | `/dev/analytics/<slug>` | Get link analytics |
| GET | `/dev/stats/<slug>` | Get link statistics |
| GET | `/dev/health` | Health check |

## 🏗️ Architecture

### Frontend (React + Vite)
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Deployment**: Served with `serve` package

### Backend (Flask)
- **Framework**: Flask with CORS support
- **Server**: Gunicorn WSGI server
- **Storage**: File-based JSON storage
- **Architecture**: Clean architecture with separated layers

## 🐳 Docker Optimizations

### Frontend Optimizations
- Multi-stage build (reduces image size by ~60%)
- Alpine Linux base (minimal OS footprint)
- Non-root user for security
- Health checks for monitoring
- Static file serving with `serve`

### Backend Optimizations
- Python slim image (smaller than full Python)
- Single layer dependency installation
- Production WSGI server (Gunicorn)
- Non-root user for security
- Comprehensive health checks

## 🛠️ Development

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Local Development Setup

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Backend
```bash
cd backend
pip install -r requirements.txt
python local_server.py
```

### Running Tests
```bash
cd backend
python -m pytest tests/
```

## 📁 Project Structure

```
LinkPulse/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.jsx         # Main app component
│   │   └── main.jsx        # Entry point
│   ├── Dockerfile          # Frontend container
│   └── package.json        # Dependencies
├── backend/                 # Flask backend
│   ├── src/                # Source code
│   │   ├── data_layer.py   # Data access layer
│   │   ├── logic_layer.py  # Business logic
│   │   ├── models.py       # Data models
│   │   └── services.py     # Service layer
│   ├── tests/              # Test suite
│   ├── Dockerfile          # Backend container
│   └── requirements.txt    # Python dependencies
├── docker-compose.yml      # Multi-container setup
└── README.md              # This file
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow existing code style and patterns
- Add tests for new features
- Update documentation as needed
- Ensure Docker builds pass
- Test both frontend and backend changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with modern web technologies
- Containerized for easy deployment
- Designed for scalability and maintainability

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Contribute improvements via pull requests

---

**Made with ❤️ by the LinkPulse community**