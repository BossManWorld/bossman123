# Docker Commands Cheat Sheet

## Core Concepts
# Image  = the blueprint (like a class)
# Container = a running instance of an image (like an object)
# Dockerfile = instructions to build an image
# Docker Hub = cloud registry to store and share images

## Dockerfile Structure
FROM python:3.11-slim          # base image
WORKDIR /app                   # set working directory
COPY requirements.txt .        # copy file into image
RUN pip install -r requirements.txt   # run command during build
COPY . .                       # copy all project files
EXPOSE 5000                    # document which port the app uses
CMD ["python", "app.py"]       # command to run when container starts

## Building Images
docker build -t flask-api:v1 .            # build image, tag as flask-api:v1
docker build -t myname/flask-api:latest . # build with Docker Hub tag
docker images                             # list all local images
docker rmi flask-api:v1                   # delete an image

## Running Containers
docker run flask-api:v1                   # run (blocks terminal)
docker run -d flask-api:v1               # detached (background)
docker run -d -p 5000:5000 flask-api:v1  # map host port to container port
docker run -d -p 5000:5000 --name flask-api flask-api:v1   # named container
docker run -d -p 5000:5000 --restart=always --name flask-api flask-api:v1

## Managing Containers
docker ps                                 # list running containers
docker ps -a                              # list ALL containers (inc. stopped)
docker stop flask-api                     # gracefully stop container
docker start flask-api                    # start a stopped container
docker restart flask-api                  # restart container
docker rm flask-api                       # delete stopped container
docker stop flask-api && docker rm flask-api   # stop + delete in one line

## Logs & Debugging
docker logs flask-api                     # show container logs
docker logs -f flask-api                  # follow logs live (like tail -f)
docker logs --tail 50 flask-api           # last 50 lines only
docker stats flask-api                    # live CPU/memory usage
docker exec -it flask-api bash            # open shell inside running container
docker inspect flask-api                  # detailed container info

## Docker Hub (Registry)
docker login                              # log in to Docker Hub
docker push myname/flask-api:latest      # push image to Docker Hub
docker pull myname/flask-api:latest      # pull image from Docker Hub

## Nuclear Reset (when everything breaks)
docker stop flask-api || true
docker rm flask-api || true
docker pull myname/flask-api:latest
docker run -d -p 5000:5000 --restart=always --name flask-api myname/flask-api:latest
docker ps

## Docker Compose (if exam asks about it)
# docker-compose.yml
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    restart: always

docker compose up -d          # start all services in background
docker compose down           # stop and remove all services
docker compose logs -f        # follow logs for all services
docker compose ps             # list compose services
