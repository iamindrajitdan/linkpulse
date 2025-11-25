# EC2 Deployment Guide

## Quick Fix Summary

The issue was that your Flask server was binding to `localhost` (127.0.0.1) only, making it inaccessible from external connections. Fixed by binding to `0.0.0.0`.

## 1. Security Group Setup

Create security group with these inbound rules:
```bash
# Create security group
aws ec2 create-security-group \
  --group-name linkpulse-sg \
  --description "LinkPulse application security group"

# Add rules
aws ec2 authorize-security-group-ingress \
  --group-name linkpulse-sg \
  --protocol tcp --port 22 --cidr 0.0.0.0/0    # SSH
  
aws ec2 authorize-security-group-ingress \
  --group-name linkpulse-sg \
  --protocol tcp --port 3000 --cidr 0.0.0.0/0  # Frontend
  
aws ec2 authorize-security-group-ingress \
  --group-name linkpulse-sg \
  --protocol tcp --port 5000 --cidr 0.0.0.0/0  # Backend API
```

## 2. EC2 Instance Setup

```bash
# SSH into your EC2 instance
ssh -i your-key.pem ec2-user@YOUR_EC2_PUBLIC_IP

# Run deployment script
chmod +x deploy-ec2.sh
./deploy-ec2.sh
```

## 3. Manual Setup (Alternative)

### Backend Fix
```bash
# The key fix - bind to all interfaces
app.run(debug=True, port=5000, host='0.0.0.0')
```

### Frontend Configuration
```bash
# Update .env.production with your EC2 IP
echo "VITE_API_BASE_URL=http://YOUR_EC2_PUBLIC_IP:5000/dev" > frontend/.env.production

# Build and serve
cd frontend
npm run build
npx serve -s dist -l 3000
```

### Start Services
```bash
# Backend
cd backend
python3 local_server.py &

# Frontend  
cd frontend
npx serve -s dist -l 3000 &
```

## 4. Verification

Test the deployment:
```bash
# Health check
curl http://YOUR_EC2_PUBLIC_IP:5000/dev/health

# Frontend
curl http://YOUR_EC2_PUBLIC_IP:3000
```

## 5. Production Considerations

- Use PM2 for process management
- Set up nginx reverse proxy
- Configure SSL certificates
- Use environment variables for sensitive data
- Set up monitoring and logging

## Troubleshooting

1. **Connection refused**: Check security group rules
2. **CORS errors**: Verify backend CORS configuration  
3. **404 errors**: Ensure services are running on correct ports
4. **Environment variables**: Check .env files are loaded correctly