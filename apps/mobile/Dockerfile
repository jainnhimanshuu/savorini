FROM node:18-alpine

# Install dependencies for Expo CLI
RUN npm install -g @expo/cli

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./
COPY packages/types/package.json ./packages/types/

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build types package
RUN npm run build --workspace=@happyhour/types

# Expose port for Expo dev server
EXPOSE 8081

# Start Expo dev server
CMD ["npx", "expo", "start", "--web", "--port", "8081"]
