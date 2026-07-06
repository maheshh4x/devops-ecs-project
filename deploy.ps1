# ==============================================================================
# AWS ECS + ECR Deployment Script for Windows PowerShell
# Run this script step by step. Replace ACCOUNT_ID with your AWS Account ID.
# ==============================================================================

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION — Edit these values before running
# ─────────────────────────────────────────────────────────────────────────────
$REGION        = "us-east-1"
$ACCOUNT_ID    = "250492956933"
$REPO_NAME     = "my-ecs-app"
$CLUSTER_NAME  = "my-ecs-cluster"
$SERVICE_NAME  = "my-app-service"
$IMAGE_TAG     = "latest"
$ECR_URI       = "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  AWS ECS + ECR Deployment Script" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: Verify tools are installed
# ─────────────────────────────────────────────────────────────────────────────
Write-Host "`n[STEP 1] Verifying tools..." -ForegroundColor Yellow
docker --version
aws --version

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: Build Docker image locally
# ─────────────────────────────────────────────────────────────────────────────
Write-Host "`n[STEP 2] Building Docker image..." -ForegroundColor Yellow
docker build -t $REPO_NAME .

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3: Create ECR Repository
# ─────────────────────────────────────────────────────────────────────────────
Write-Host "`n[STEP 3] Creating ECR repository..." -ForegroundColor Yellow
aws ecr create-repository `
    --repository-name $REPO_NAME `
    --region $REGION `
    --image-scanning-configuration scanOnPush=true

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4: Authenticate Docker to ECR
# ─────────────────────────────────────────────────────────────────────────────
Write-Host "`n[STEP 4] Logging Docker into ECR..." -ForegroundColor Yellow
aws ecr get-login-password --region $REGION | `
    docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5: Tag and Push image to ECR
# ─────────────────────────────────────────────────────────────────────────────
Write-Host "`n[STEP 5] Tagging and pushing image to ECR..." -ForegroundColor Yellow
docker tag "${REPO_NAME}:latest" "${ECR_URI}:${IMAGE_TAG}"
docker push "${ECR_URI}:${IMAGE_TAG}"

# ─────────────────────────────────────────────────────────────────────────────
# STEP 6: Create ECS Cluster
# ─────────────────────────────────────────────────────────────────────────────
Write-Host "`n[STEP 6] Creating ECS cluster..." -ForegroundColor Yellow
aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $REGION

# ─────────────────────────────────────────────────────────────────────────────
# STEP 7: Create CloudWatch Log Group
# ─────────────────────────────────────────────────────────────────────────────
Write-Host "`n[STEP 7] Creating CloudWatch log group..." -ForegroundColor Yellow
aws logs create-log-group --log-group-name "/ecs/$REPO_NAME" --region $REGION

# ─────────────────────────────────────────────────────────────────────────────
# STEP 8: Register Task Definition (update ACCOUNT_ID in task-definition.json first)
# ─────────────────────────────────────────────────────────────────────────────
Write-Host "`n[STEP 8] Registering task definition..." -ForegroundColor Yellow
# First update the task-definition.json with your account ID
(Get-Content task-definition.json) -replace 'ACCOUNT_ID', $ACCOUNT_ID | Set-Content task-definition.json
aws ecs register-task-definition --cli-input-json file://task-definition.json --region $REGION

Write-Host "`n[DONE] Script finished! Now create Load Balancer + ECS Service via AWS Console." -ForegroundColor Green
Write-Host "See README.md for next steps." -ForegroundColor Green
