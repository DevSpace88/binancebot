FROM node:16-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install
# Installiere chart.js explizit
RUN npm install chart.js@latest

# Copy source code
COPY . .

# Expose port
EXPOSE 8080

# Start development server
CMD ["npm", "run", "serve"]