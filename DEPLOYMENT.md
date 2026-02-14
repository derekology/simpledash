# Production Deployment Guide

## Overview

This guide covers deploying Simple Dash to a production environment using Docker.

## Quick Start (Recommended)

The easiest way to deploy Simple Dash is using the pre-built Docker image:

### 1. Download docker-compose file

```bash
# Create directory
mkdir simpledash && cd simpledash

# Download docker-compose file
curl -O https://raw.githubusercontent.com/derekology/simpledash/main/docker-compose.hub.yml

# Rename to docker-compose.yml
mv docker-compose.hub.yml docker-compose.yml
```

### 2. Create environment file (optional)

```bash
cat > .env << EOF
PORT=8000
MAX_FILE_SIZE=10485760
MAX_FILES=12
DEV=False
EOF
```

### 3. Start the application

```bash
docker compose up -d
```

That's it! Simple Dash is now running on port 8000.

### 4. Verify it's working

```bash
curl http://localhost:8000/health
```

---

## Alternative: Build from Source

If you prefer to build from source instead of using the Docker Hub image:

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Domain name (for SSL)
- Reverse proxy (nginx recommended)

### 1. Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose (if not included)
sudo apt install docker-compose-plugin
```

### 2. Application Deployment

```bash
# Clone repository
git clone https://github.com/derekology/simpledash.git
cd simpledash

# Configure environment
cp .env.example .env
nano .env  # Edit as needed

# Build and start
docker compose up -d

# Check status
docker compose ps
docker compose logs
```

### 3. Environment Configuration

Edit `.env` for production:

```bash
PORT=8000
MAX_FILE_SIZE=10485760  # 10MB
MAX_FILES=12
DEV=False
```

### 4. Start Application

```bash
docker compose up -d
```

## Reverse Proxy Setup

### Nginx

**Install nginx:**

```bash
sudo apt install nginx
```

**Create nginx configuration:**

```bash
sudo nano /etc/nginx/sites-available/simpledash
```

**Add configuration:**

```nginx
server {
    listen 80;
    server_name dash.example.com;

    # Increase upload size limits
    client_max_body_size 120M;
    client_body_timeout 300s;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts for large file uploads
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

**Enable site:**

```bash
sudo ln -s /etc/nginx/sites-available/simpledash /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL/TLS Setup

### Using Certbot (with Nginx)

**Install Certbot:**

```bash
sudo apt install certbot python3-certbot-nginx
```

**Get certificate:**

```bash
sudo certbot --nginx -d dash.example.com
```

**Auto-renewal:**

```bash
# Test renewal
sudo certbot renew --dry-run

# Renewal happens automatically via systemd timer
sudo systemctl status certbot.timer
```

## Cloud Platforms

### AWS ECS

1. Push Docker image to ECR
2. Create ECS task definition
3. Create ECS service with ALB
4. Configure Route53 for DNS

### Google Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/simpledash

# Deploy
gcloud run deploy simpledash \
  --image gcr.io/PROJECT_ID/simpledash \
  --platform managed \
  --allow-unauthenticated \
  --port 8000 \
  --max-instances 10
```

### DigitalOcean App Platform

1. Connect GitHub repository
2. Configure build settings
3. Set environment variables
4. Deploy

## Configuration

### Environment Variables

| Variable        | Default    | Description          |
| --------------- | ---------- | -------------------- |
| `PORT`          | `8000`     | Server port          |
| `MAX_FILE_SIZE` | `10485760` | Max file size (10MB) |
| `MAX_FILES`     | `12`       | Max files per upload |
| `DEV`           | `False`    | Development mode     |

Production-ready `.env` file:

```env
PORT=8000
MAX_FILE_SIZE=10485760
MAX_FILES=12
DEV=False
```

### Reverse Proxy Configuration

Complete nginx configuration with security headers:

```nginx
server {
    listen 443 ssl http2;
    server_name dash.example.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/dash.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dash.example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Upload limits
    client_max_body_size 120M;
    client_body_timeout 300s;
    client_header_timeout 300s;

    # Proxy configuration
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
        proxy_buffering off;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name dash.example.com;
    return 301 https://$server_name$request_uri;
}
```

## Security Considerations

### 1. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### 2. Container Security

- Run as non-root user (already configured in Dockerfile)
- Keep base images updated
- Scan for vulnerabilities: `docker scout cves simpledash`

### 3. Application Security

- Files are processed but not stored persistently
- Implement rate limiting at nginx level
- Monitor for unusual upload patterns

### 4. Rate Limiting (nginx)

```nginx
http {
    limit_req_zone $binary_remote_addr zone=upload:10m rate=5r/m;

    server {
        # ... other config

        location /parse {
            limit_req zone=upload burst=2;
            proxy_pass http://localhost:8000;
        }
    }
}
```

## Monitoring

### Health Checks

```bash
# Check application health
curl http://localhost:8000/health

# Check container health
docker inspect --format='{{.State.Health.Status}}' simpledash
```

### Logging

```bash
# View real-time logs
docker compose logs -f

# View last 100 lines
docker compose logs --tail=100

# Follow specific service
docker compose logs -f simpledash
```

### System Monitoring

```bash
# Container resource usage
docker stats simpledash

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Backup and Recovery

### Backup Strategy

Simple Dash doesn't store data persistently, but you should backup:

1. Configuration files (`.env`, `docker-compose.yml`)
2. Custom nginx configuration
3. SSL certificates (handled by certbot)

```bash
# Backup configuration
tar -czf simpledash-config-$(date +%Y%m%d).tar.gz .env docker-compose.yml
```

## Scaling

### Horizontal Scaling

Run multiple instances behind a load balancer:

```yaml
# docker-compose.yml
services:
  simpledash-1:
    build: .
    container_name: simpledash-1
    ports:
      - "8001:8000"

  simpledash-2:
    build: .
    container_name: simpledash-2
    ports:
      - "8002:8000"
```

**nginx load balancer:**

```nginx
upstream simpledash {
    server localhost:8001;
    server localhost:8002;
}

server {
    location / {
        proxy_pass http://simpledash;
    }
}
```

### Vertical Scaling

Adjust resource limits:

```yaml
services:
  simpledash:
    deploy:
      resources:
        limits:
          cpus: "2"
          memory: 2G
```

## Maintenance

## Updates and Maintenance

### Update Application

**Using Docker Hub image:**

```bash
docker compose pull
docker compose up -d
```

**From source:**

```bash
# Pull latest changes
git pull

# Rebuild and restart
docker compose down
docker compose build --no-cache
docker compose up -d

# Verify
docker compose ps
docker compose logs
```

### Update Dependencies

```bash
# Update Python dependencies
pip list --outdated
# Update requirements.txt as needed

# Update Node dependencies
cd frontend
npm outdated
# Update package.json as needed
```

### Zero-Downtime Updates

```bash
# Build new image
docker compose build

# Start new container on different port
docker compose up -d --scale simpledash=2

# Update nginx to use new instance
# Update docker-compose to use new image
# Stop old container
```

## Troubleshooting

### Common Issues

**1. Container won't start**

```bash
docker compose logs
# Check port conflicts
sudo netstat -tulpn | grep 8000
```

**2. 502 Bad Gateway**

```bash
# Check if container is running
docker compose ps

# Check nginx configuration
sudo nginx -t
```

**3. File upload fails**

```bash
# Check nginx upload size
grep client_max_body_size /etc/nginx/sites-available/simpledash

# Check container logs
docker compose logs | grep -i error
```

**4. High memory usage**

```bash
# Check container stats
docker stats simpledash

# Restart container
docker compose restart
```

## Performance Optimization

### Nginx Caching

```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Gzip Compression

```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
gzip_min_length 1000;
```

## Support

For deployment issues:

- Check logs: `docker compose logs`
- Review nginx logs: `/var/log/nginx/error.log`
- Test configuration: `nginx -t`
- Check Docker status: `docker compose ps`
