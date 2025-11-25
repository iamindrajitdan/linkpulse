# Multi-stage build for optimized image size
FROM node:18-alpine AS build

WORKDIR /app

# Accept build argument for API URL
ARG VITE_API_BASE_URL=http://localhost:5000/dev
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Copy package files first for better caching
COPY package*.json ./

# Install all dependencies (including dev dependencies for build)
RUN npm ci --silent

# Copy source code
COPY . .

# Build the application with environment variable
RUN npm run build

# Production stage with minimal image
FROM node:18-alpine

WORKDIR /app

# Install serve globally
RUN npm install -g serve@14 --silent

# Copy built assets from builder stage
COPY --from=build /app/dist ./dist

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Change ownership of app directory
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

# Start the application
CMD ["serve", "-s", "dist", "-l", "3000"]