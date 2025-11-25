#!/bin/bash

# EC2 Deployment Script for LinkPulse
# Run this on your EC2 instance

set -e

echo "🚀 Starting LinkPulse deployment on EC2..."

# Update system
sudo yum update -y

# Install Node.js and npm
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# Install Python 3 and pip
sudo yum install -y python3 python3-pip

# Install PM2 for process management
sudo npm install -g pm2

# Get EC2 public IP
EC2_PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo "📍 EC2 Public IP: $EC2_PUBLIC_IP"

# Clone repository (if not already present)
if [ ! -d "linkpulse" ]; then
    git clone https://github.com/iamindrajitdan/linkpulse.git
fi

cd linkpulse

# Backend setup
echo "🔧 Setting up backend..."
cd backend
pip3 install -r requirements.txt
cd ..

# Frontend setup
echo "🔧 Setting up frontend..."
cd frontend

# Update production environment with EC2 IP
echo "VITE_API_BASE_URL=http://$EC2_PUBLIC_IP:5000/dev" > .env.production

npm install
npm run build
cd ..

# Start services with PM2
echo "🚀 Starting services..."

# Start backend
pm2 start backend/local_server.py --name "linkpulse-backend" --interpreter python3

# Start frontend (serve build files)
pm2 serve frontend/dist 3000 --name "linkpulse-frontend"

# Save PM2 configuration
pm2 save
pm2 startup

echo "✅ Deployment complete!"
echo "🌐 Frontend: http://$EC2_PUBLIC_IP:3000"
echo "🔧 Backend API: http://$EC2_PUBLIC_IP:5000/dev"
echo "❤️ Health Check: http://$EC2_PUBLIC_IP:5000/dev/health"