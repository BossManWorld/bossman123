# AWS EC2 & Deployment Cheat Sheet

## SSH Into EC2
chmod 400 ~/.ssh/devops-key.pem          # fix key permissions (MUST do first)
ssh -i ~/.ssh/devops-key.pem ubuntu@YOUR_PUBLIC_IP

## First-Time Server Setup (run once after SSH)
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo usermod -aG docker ubuntu
newgrp docker
docker --version                          # verify install

## Deploy Manually on EC2
docker pull YOUR_DOCKERHUB_USERNAME/flask-api:latest
docker run -d \
  -p 5000:5000 \
  --restart=always \
  --name flask-api \
  YOUR_DOCKERHUB_USERNAME/flask-api:latest
docker ps

## Verify App is Live (run from YOUR LOCAL machine)
curl http://YOUR_EC2_IP:5000/api/health
curl http://YOUR_EC2_IP:5000/api/students
curl -X POST http://YOUR_EC2_IP:5000/api/students \
  -H 'Content-Type: application/json' \
  -d '{"name": "Yahya", "grade": "A"}'

## Security Group Ports (set in AWS console)
Port 22   → SSH (set source to My IP)
Port 5000 → Flask API (source 0.0.0.0/0)
Port 80   → HTTP (source 0.0.0.0/0)
Port 443  → HTTPS (source 0.0.0.0/0)

## EC2 Key Terms
Instance     = a virtual machine on AWS
AMI          = the OS template (Ubuntu 22.04)
t2.micro     = free tier instance type (1 vCPU, 1GB RAM)
Security Group = firewall rules for the instance
Key Pair     = .pem file used to SSH in
Public IP    = internet-facing address of your instance
Elastic IP   = static IP that doesn't change on restart

## Monitoring Your Running App
docker ps                                 # is container running?
docker logs -f flask-api                  # live logs
docker stats flask-api                    # CPU/memory usage
ss -tulnp | grep :5000                    # is port open?
free -h && df -h && uptime                # server health

## Restart Container After EC2 Reboot
# If you used --restart=always, Docker does this automatically
# To verify after reboot:
ssh -i ~/.ssh/devops-key.pem ubuntu@YOUR_PUBLIC_IP
docker ps                                 # should show flask-api running
curl http://localhost:5000/api/health     # should return {"status": "ok"}

## Transfer Files to EC2 (scp)
# Run this on YOUR LOCAL machine:
scp -i ~/.ssh/devops-key.pem app.py ubuntu@YOUR_EC2_IP:~/
scp -i ~/.ssh/devops-key.pem -r ~/devops/week5/ ubuntu@YOUR_EC2_IP:~/flask-api/
# scp = secure copy  |  -r = recursive (copies whole folder)
