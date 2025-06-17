# 🐳 Docker, Dockerfile & Docker Compose Cheatsheet

## Table of Contents

- [🐳 Docker, Dockerfile & Docker Compose Cheatsheet](#-docker-dockerfile--docker-compose-cheatsheet)
    - [🧱 Docker CLI](#-docker-cli)
        - [🔹 Image Commands](#-image-commands)
        - [🔹 Container Commands](#-container-commands)
        - [🔹 Volume and Network](#-volume-and-network)
        - [🔹 Clean-up](#-clean-up)
    - [📦 Dockerfile](#-dockerfile)
        - [🔹 Common Instructions](#-common-instructions)
    - [⚙️ Docker Compose](#-docker-compose)
        - [🔹 Compose CLI](#-compose-cli)
    - [🌐 Networking, Ingress, and Service Accounts](#-networking-ingress-and-service-accounts)
        - [🔹 Expose Service with Ingress (via Docker Desktop or Traefik)](#-expose-service-with-ingress-via-docker-desktop-or-traefik)
        - [🔹 Using a Custom Network](#-using-a-custom-network)
    - [🔐 Docker with Service Account (Kubernetes Context)](#-docker-with-service-account-kubernetes-context)
    - [🛠️ Tips](#-tips)
    - [📎 References](#-references)


---

## 🧱 Docker CLI
### 🔹 Image Commands
```bash
docker build -t myimage:tag .       # Build image from Dockerfile
docker images                       # List local images
docker rmi myimage                  # Remove image
docker pull nginx:latest            # Pull image from Docker Hub
```
### 🔹 Container Commands
```bash
docker run -d -p 8080:80 myimage    # Run container in detached mode
docker ps                           # List running containers
docker ps -a                        # List all containers (even stopped)
docker stop <container_id>          # Stop container
docker rm <container_id>            # Remove container
docker exec -it <cid> bash          # Shell into running container
docker logs -f <cid>                # Stream container logs
```
### 🔹 Volume and Network
```bash
docker volume ls                    # List volumes
docker volume create myvol          # Create named volume
docker network ls                   # List networks
docker network create mynet         # Create custom network
```
### 🔹 Clean-up
```bash
docker system prune -a              # Remove unused images/containers/networks
```
---
## 📦 Dockerfile
```Dockerfile
# Base image
FROM python:3.11-slim
# Metadata
LABEL maintainer="yourname@example.com"
# Set workdir
WORKDIR /app
# Copy source
COPY . .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Expose port
EXPOSE 8000
# Default command
CMD ["python", "main.py"]
```
### 🔹 Common Instructions
| Directive     | Description                          |
|---------------|--------------------------------------|
| `FROM`        | Base image                           |
| `COPY`        | Copy files into image                |
| `RUN`         | Execute command during build         |
| `CMD`         | Default command for container        |
| `ENTRYPOINT`  | Define main command (more strict)    |
| `ENV`         | Set environment variables            |
| `EXPOSE`      | Inform about listening port          |
| `WORKDIR`     | Set working directory inside image   |
| `VOLUME`      | Declare mount point                  |
---
## ⚙️ Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - ENV=dev
    depends_on:
      - redis
  redis:
    image: redis:alpine
```
### 🔹 Compose CLI
```bash
docker-compose up -d              # Start services
docker-compose down               # Stop and clean up
docker-compose build              # Build services
docker-compose logs -f app        # View logs
docker-compose exec app bash      # Shell into container
```
---
## 🌐 Networking, Ingress, and Service Accounts
### 🔹 Expose Service with Ingress (via Docker Desktop or Traefik)
```yaml
services:
  web:
    image: nginx
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.web.rule=Host(`myapp.local`)"
      - "traefik.http.services.web.loadbalancer.server.port=80"
    networks:
      - webnet
networks:
  webnet:
```
### 🔹 Using a Custom Network
```bash
docker network create my_custom_net
docker run -d --network my_custom_net myapp
```
---
## 🔐 Docker with Service Account (Kubernetes Context)
> Not directly Docker, but when using `docker build` in CI/CD for Kubernetes:
- Mount a GCP service account:
```bash
gcloud auth activate-service-account --key-file=key.json
```
- Use `gcloud auth configure-docker` to allow pushing to GCR
---
## 🛠️ Tips
- Use `.dockerignore` to exclude files from context
- Use `multi-stage builds` to reduce final image size
- Prefer minimal base images (`alpine`, `distroless`)
- Validate `docker-compose.yaml` with `docker-compose config`
---
## 📎 References
- [Docker Docs](https://docs.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)
