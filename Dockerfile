# Use Node.js 22 LTS Alpine as base image for a smaller footprint
FROM node:22-alpine

# Set working directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package*.json ./

# Install production dependencies
RUN npm ci --only=production

# Copy source code and other necessary files
COPY src/ ./src/
COPY .env_example ./.env

# Create logs directory
RUN mkdir -p logs

# Expose port (default 3000 according to app.js)
EXPOSE 3000

# Set user to node for better security context
USER node

# Start the application
CMD ["npm", "start"]
