# Journal App Deployment

This project automates the deployment of the **Journal App** using **AWS**, **Terraform**, **Docker**, and **CI/CD pipelines**. Originally set up manually using **AWS Console**, the process has been automated to provide a secure, scalable, and streamlined deployment.

<br>

## Overview

The **Journal App** is a containerised Django application deployed on **AWS ECS Fargate**. The deployment process is fully automated using **CI/CD pipeline** to handle Docker image building, security scans, and deployment to AWS through **Terraform**.

<br>

## Architecture Diagram

![AD](https://raw.githubusercontent.com/JunedConnect/project-charlie/main/images/Architecture%20Diagram.png)

<br>

## Key Components:

- **Dockerisation**: The app is containerised using a **Dockerfile** for consistency across environments.

- **Secrets Management**: AWS Secrets Manager is used to securely store a secret required by the application.

- **Infrastructure as Code (IaC)**: Terraform provisions the following AWS resources:
    - **ECS Fargate** for serverless container orchestration.
    - **Application Load Balancer (ALB)** for routing HTTP/HTTPS traffic.
    - **Route 53** for custom domain name mapping.
    - **Security Groups** to control network access.
    - **VPC, Subnets, and Internet Gateway** to establish the network architecture.

- **CI/CD Pipeline**: GitHub Actions automate:
    - **Building and pushing the Docker image** to **Amazon ECR**.
    - **Applying Terraform** to deploy or update AWS infrastructure.
    - **Performing security and compliance scans** to ensure code quality and security.
    - **Destroying Terraform resources** when necessary.

<br>

## Directory Structure

```
./
├── app
│   └── Dockerfile
├── terraform
│   ├── modules
│   │   ├── alb
│   │   ├── ecs
│   │   ├── network
│   │   └── route53
│   ├── main.tf
│   ├── provider.tf
│   └── variables.tf
└── .github
    └── workflows
        ├── DockerBuild&Deploy.yml
        ├── TerraformBuild.yml
        ├── TerraformApply.yml
        └── TerraformDestroy.yml
```

- **Docker Files** (`app/`):
    - **Dockerfile**: Defines the app's containerised environment.

- **Terraform Files** (`terraform/`):
    - **modules/alb**: Sets up the **Application Load Balancer** (ALB).
    - **modules/ecs**: Configures the **ECS Cluster** and **Fargate service**.
    - **modules/network**: Provisions **Security Groups**, **VPC**, and **Subnets**.
    - **modules/route53**: Manages **Route 53 DNS records** and **SSL certificates**.
    - **main.tf**: Defines the AWS infrastructure using Terraform modules.
    - **provider.tf**: Specifies the AWS provider configuration.
    - **variables.tf**: Stores configurable values for the Terraform setup.

- **CI/CD Pipelines (`.github/workflows/`)**:
    - **DockerBuild&Deploy.yml**:
        - Builds and pushes the Docker image to **ECR**.
        - Runs **Trivy** to scan the image for vulnerabilities.
    
    - **TerraformPlan.yml**:
        - Previews the Terraform configuration to provision AWS resources.
        - Runs **TFLint** and **Checkov** for security and syntax checks.
    
    - **TerraformApply.yml**:
        - Applies the Terraform configuration to provision AWS resources.
    
    - **TerraformDestroy.yml**:
        - Destroys Terraform-managed infrastructure.

<br>

## Prerequisites

### 1. AWS Secrets Manager Setup

Before deploying the Django application, you must manually create a secret in AWS Secrets Manager. The Django app will automatically retrieve this secret during deployment and use it for the entire duration the application is active.

Please use the following values for when you set up your secret:

- **Secret Name:** `django/production/key`
- **Secret Key:** `DJANGO_SECRET_KEY`
- **Secret Value:** `<place any value here>`

### 2. Whitelisting Your Domain

To allow users to access the application via your domain, add your domain to the `CSRF_TRUSTED_ORIGINS` section within `app/digital_journal/settings.py`.

<br>

## CI/CD Deployment Workflow

The deployment process is fully automated via GitHub Actions:

1. **Docker Image Build & Deployment** (`DockerBuild&Deploy.yml`):
    - Builds the Docker image.
    - Runs **Trivy** to scan for critical vulnerabilities before pushing to ECR.
    - Pushes the image to **Amazon ECR**.

2. **Terraform Build** (`TerraformBuild.yml`):
    - Initialises the Terraform directory.
    - Previews the necessary AWS resources (ECS, ALB, Route 53, VPC, Security Groups).
    - Runs **TFLint** to validate Terraform syntax and best practices.
    - Runs **Checkov** to scan for security issues within Terraform code.
    
3. **Terraform Apply** (`TerraformApply.yml`):
    - Initialises the Terraform directory.
    - Provisions the necessary AWS resources (ECS, ALB, Route 53, VPC, Security Groups).
    
4. **Terraform Destroy** (`TerraformDestroy.yml`):
    - Destroys all Terraform-managed resources when necessary.

<br>

To trigger any of these workflows, go to **GitHub Actions** and manually run the desired workflow.


|Here’s what it will look like:|
|-------|
|Application Home Page:|
| ![App1](https://raw.githubusercontent.com/JunedConnect/project-charlie/main/images/Application%20Home%20Page.png) |
|Application Sign-up Page:|
| ![App2](https://raw.githubusercontent.com/JunedConnect/project-charlie/main/images/Sign-up%20Page.png) |
|Application Dashboard:|
| ![App3](https://raw.githubusercontent.com/JunedConnect/project-charlie/main/images/Dashboard%20Page%201.png) |
| ![App4](https://raw.githubusercontent.com/JunedConnect/project-charlie/main/images/Dashboard%20Page%202.png) |
|SSL Certificate:|
| ![App5](https://raw.githubusercontent.com/JunedConnect/project-charlie/main/images/SSL%20Certificate.png) |
|CI/CD Docker Build & Push:|
| ![CICD1](https://raw.githubusercontent.com/JunedConnect/project-charlie/main/images/CICD%20Docker%20Build.png) |
|CI/CD Terraform Apply:|
| ![CICD2](https://raw.githubusercontent.com/JunedConnect/project-charlie/main/images/CICD%20Terraform%20Apply.png) |
|CI/CD Terraform Destroy:|
| ![CICD3](https://raw.githubusercontent.com/JunedConnect/project-charlie/main/images/CICD%20Terraform%20Destroy.png) |
