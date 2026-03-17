# Deployment Guide

This guide walks through every step needed to deploy the `AwsCdkLambdaApiStack`
to your AWS account from scratch.

---

## Prerequisites

| Requirement | Version | Check |
|---|---|---|
| Python | 3.11+ | `python3 --version` |
| Node.js | 18+ | `node --version` |
| AWS CDK CLI | 2.x | `cdk --version` |
| AWS CLI | 2.x | `aws --version` |
| AWS credentials | configured | `aws sts get-caller-identity` |

Install the CDK CLI globally if you haven't already:

```bash
npm install -g aws-cdk
```

---

## Step 1 — Clone and set up the project

```bash
git clone https://github.com/rman90/aws-cdk-lambda-api.git
cd aws-cdk-lambda-api

python3 -m venv .venv
source .venv/bin/activate          # Windows: source.bat

pip install -r requirements.txt
```

---

## Step 2 — Bootstrap your AWS environment

CDK bootstrap provisions an S3 bucket and ECR repository that CDK uses to
stage assets during deployment. This only needs to be run once per
AWS account/region combination.

```bash
cdk bootstrap
```

Expected output:
```
✅  Environment aws://123456789012/us-east-1 bootstrapped.
```

---

## Step 3 — Synthesize the CloudFormation template

`cdk synth` compiles your Python CDK code into a CloudFormation template
without deploying anything. Use this to inspect what will be created.

```bash
cdk synth
```

The generated template is saved to `cdk.out/AwsCdkLambdaApiStack.template.json`.

---

## Step 4 — Deploy the stack

```bash
cdk deploy
```

CDK will display a summary of IAM changes and ask for confirmation before
deploying. Type `y` to proceed.

On success you will see the API endpoint URL in the outputs:

```
Outputs:
AwsCdkLambdaApiStack.ApiEndpointUrl = https://abc123.execute-api.us-east-1.amazonaws.com/prod/
```

Save this URL — you will use it to test the API.

---

## Step 5 — Validate the deployment

```bash
# Replace with your actual endpoint URL
BASE_URL="https://abc123.execute-api.us-east-1.amazonaws.com/prod"

curl "$BASE_URL/hello"
# {"message": "Hello from AWS Lambda via API Gateway!"}

curl "$BASE_URL/health"
# {"status": "healthy"}
```

---

## Updating the stack

After making code changes, redeploy with the same command:

```bash
cdk deploy
```

CDK performs a diff and only updates the resources that changed.
To preview changes before deploying:

```bash
cdk diff
```

---

## Destroying the stack

To remove all provisioned resources and avoid ongoing charges:

```bash
cdk destroy
```

Type `y` when prompted. This deletes the CloudFormation stack and all
resources it manages.
