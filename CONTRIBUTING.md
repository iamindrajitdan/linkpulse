# Contributing to LinkPulse

Thank you for your interest in contributing to LinkPulse! This document provides guidelines and information for contributors.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/linkpulse.git
   cd linkpulse
   ```
3. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🛠️ Development Setup

### Using Docker (Recommended)
```bash
docker-compose up --build
```

### Local Development
```bash
# Frontend
cd frontend && npm install && npm run dev

# Backend
cd backend && pip install -r requirements.txt && python local_server.py
```

## 📝 Contribution Guidelines

### Code Style
- Follow existing code patterns and conventions
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions small and focused

### Testing
- Add tests for new features
- Ensure existing tests pass
- Run tests before submitting PR:
  ```bash
  cd backend && python -m pytest tests/
  ```

### Docker
- Test Docker builds locally
- Ensure both services start correctly
- Verify health checks pass

## 🔄 Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure Docker builds** pass
4. **Create descriptive PR title** and description
5. **Link related issues** if applicable

## 🐛 Bug Reports

When reporting bugs, please include:
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Docker version)
- Relevant logs or error messages

## 💡 Feature Requests

For new features:
- Describe the use case
- Explain the expected behavior
- Consider implementation approach
- Discuss potential breaking changes

## 📋 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain a welcoming environment

## 🏷️ Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to docs
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed

## 🎯 Areas for Contribution

- Frontend UI/UX improvements
- Backend API enhancements
- Docker optimization
- Documentation updates
- Test coverage
- Performance improvements
- Security enhancements

Thank you for contributing to LinkPulse! 🙏