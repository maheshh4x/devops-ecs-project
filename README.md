# 🚀 DevOps Project — Deploying a Containerized App on AWS ECS + ECR

> **Internship Project** | Docker + AWS ECR + AWS ECS + Load Balancer + CI/CD

---

## 📖 Project Overview

This project deploys a Python Flask web application as a Docker container on **AWS ECS (Elastic Container Service)** using **AWS ECR (Elastic Container Registry)** for image storage, with a **Load Balancer** for high availability and **GitHub Actions** for CI/CD automation.

---

## 🏗️ Architecture

```
Developer (Push Code)
        │
        ▼
  GitHub Actions (CI/CD)
        │
        ├──► Build Docker Image
        │
        ├──► Push to AWS ECR (Elastic Container Registry)
        │
        └──► Update AWS ECS Service
                    │
                    ▼
          Application Load Balancer
                    │
              ┌─────┴──────┐
              ▼            ▼
          ECS Task      ECS Task
         (Container)   (Container)
              │            │
              └─────┬──────┘
                    ▼
               EC2 Instance
```

---

## 📁 Project Structure

```
devops-ecs-project/
├── app/
│   ├── app.py                    # Flask web application
│   └── requirements.txt          # Python dependencies
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Actions CI/CD pipeline
├── Dockerfile                    # Container build instructions
├── .dockerignore                 # Files to exclude from Docker build
├── task-definition.json          # ECS Task Definition
├── deploy.ps1                    # Windows PowerShell deployment script
└── README.md                     # This file
```

---

## 🛠️ Prerequisites

Install these tools before starting:

| Tool | Download Link | Verify Command |
|------|--------------|----------------|
| Docker Desktop | https://www.docker.com/products/docker-desktop/ | `docker --version` |
| AWS CLI v2 | https://aws.amazon.com/cli/ | `aws --version` |
| Git | https://git-scm.com/ | `git --version` |

---

## 🔢 Step-by-Step Setup Guide

### ✅ Step 1 — Configure AWS CLI

```powershell
aws configure
```
Enter your:
- **AWS Access Key ID** (from AWS Console → IAM → Users → Security Credentials)
- **AWS Secret Access Key**
- **Default region**: `ap-south-1`
- **Output format**: `json`

---

### ✅ Step 2 — Build Docker Image Locally

```powershell
cd "c:\devops internship\devops-ecs-project"
docker build -t my-ecs-app .
```

### ✅ Step 3 — Test Docker Image Locally

```powershell
docker run -p 5000:5000 my-ecs-app
```
Open browser → http://localhost:5000 ✅

---

### ✅ Step 4 — Create ECR Repository

```powershell
aws ecr create-repository --repository-name my-ecs-app --region ap-south-1
```

---

### ✅ Step 5 — Push Image to ECR

```powershell
# Replace YOUR_ACCOUNT_ID with your actual AWS Account ID
$ACCOUNT_ID = "YOUR_ACCOUNT_ID"
$REGION = "ap-south-1"

# Login
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"

# Tag
docker tag my-ecs-app:latest "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/my-ecs-app:latest"

# Push
docker push "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/my-ecs-app:latest"
```

---

### ✅ Step 6 — Create ECS Cluster

```powershell
aws ecs create-cluster --cluster-name my-ecs-cluster --region ap-south-1
```

---

### ✅ Step 7 — Create IAM Task Execution Role

1. Go to **AWS Console → IAM → Roles → Create Role**
2. Select **AWS service** → **Elastic Container Service Task**
3. Attach policy: `AmazonECSTaskExecutionRolePolicy`
4. Name it: `ecsTaskExecutionRole`

---

### ✅ Step 8 — Register Task Definition

```powershell
# First update ACCOUNT_ID in task-definition.json, then:
aws ecs register-task-definition --cli-input-json file://task-definition.json --region ap-south-1
```

---

### ✅ Step 9 — Create Load Balancer + ECS Service (via AWS Console)

1. Go to **EC2 → Load Balancers → Create Application Load Balancer**
2. Go to **ECS → Clusters → my-ecs-cluster → Create Service**
3. Select task definition, set desired count to **2**
4. Attach the load balancer

---

### ✅ Step 10 — Set Up CI/CD (GitHub Actions)

1. Push this project to GitHub
2. Go to **GitHub → Settings → Secrets → Actions**
3. Add secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
4. Every push to `main` will auto-deploy! 🎉

---

## 🔍 Verify Deployment

```powershell
# Check ECS service status
aws ecs describe-services --cluster my-ecs-cluster --services my-app-service --region ap-south-1

# List running tasks
aws ecs list-tasks --cluster my-ecs-cluster --region ap-south-1
```

Access your app via the **Load Balancer DNS URL** from the AWS Console.

---

## 📊 Key AWS Services Used

| Service | Purpose |
|---------|---------|
| **ECR** | Store Docker images privately |
| **ECS** | Run and manage containers |
| **EC2** | Compute instances for containers |
| **ALB** | Distribute traffic, health checks |
| **IAM** | Permissions and roles |
| **CloudWatch** | Logs and monitoring |
| **GitHub Actions** | CI/CD automation |

---

## 👨‍💻 Author

DevOps Internship Project — Built with ❤️
