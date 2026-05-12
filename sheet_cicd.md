# CI/CD & GitHub Actions Cheat Sheet

## What is CI/CD?
# CI = Continuous Integration
#   - Every git push triggers automated tests + build
#   - Catches bugs BEFORE they reach production
# CD = Continuous Delivery/Deployment
#   - Automatically deploys tested code to server
#   - No manual deployment steps needed

## Workflow File Location (CRITICAL)
# Must be at EXACTLY this path - no exceptions:
.github/workflows/ci.yml
#                 ^ note the 's' in workflows

## Workflow Triggers
on:
  push:
    branches: [ main ]          # runs on every push to main

  pull_request:
    branches: [ main ]          # runs on every PR to main

  workflow_dispatch:            # adds a manual "Run workflow" button

## Required GitHub Secrets
# Go to: Repo → Settings → Secrets and variables → Actions → New repository secret
DOCKERHUB_USERNAME    # your Docker Hub username
DOCKERHUB_TOKEN       # Docker Hub access token (not your password)
EC2_HOST              # your EC2 public IP address
EC2_SSH_KEY           # full contents of devops-key.pem file

## Full Working CI/CD Pipeline
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/flask-api:latest

      - name: Deploy to EC2
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ubuntu
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            docker pull ${{ secrets.DOCKERHUB_USERNAME }}/flask-api:latest
            docker stop flask-api || true
            docker rm flask-api || true
            docker run -d \
              -p 5000:5000 \
              --restart=always \
              --name flask-api \
              ${{ secrets.DOCKERHUB_USERNAME }}/flask-api:latest
            docker ps

## Checking Pipeline Status
# GitHub repo → Actions tab → click the latest run
# Green checkmark = passed
# Red X = failed → click it → click the failed job → read the error

## Common Pipeline Failures and Fixes

# FAILURE: "Permission denied (publickey)"
# FIX: Your EC2_SSH_KEY secret has wrong content
#      Open devops-key.pem, copy EVERYTHING including
#      -----BEGIN RSA PRIVATE KEY----- and -----END RSA PRIVATE KEY-----

# FAILURE: "Cannot connect to Docker daemon"
# FIX: Docker not installed on EC2, or ubuntu user not in docker group
#      sudo usermod -aG docker ubuntu && newgrp docker

# FAILURE: "docker: Error response from daemon: port is already allocated"
# FIX: Old container still running on port 5000
#      docker stop flask-api || true
#      docker rm flask-api || true

# FAILURE: workflow file not found / pipeline never runs
# FIX: Check folder name is .github/workflows (with s), not .github/workflow
