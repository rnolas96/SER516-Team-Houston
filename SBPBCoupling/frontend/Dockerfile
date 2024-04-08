# Stage 1: Build frontend assets
FROM node:20.11.0 AS builder

WORKDIR /app

COPY package*.json .

RUN npm install

COPY . .

RUN npm run build

# Stage 2: Install and configure Nginx to serve frontend assets
FROM nginx:alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy built frontend assets from the previous stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy Nginx configuration to enable URL rewriting
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]