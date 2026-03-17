# Architecture Explanation

## Overview

This project provisions a fully serverless API on AWS using two managed
services: Amazon API Gateway and AWS Lambda. There are no servers to manage,
no capacity to plan, and the infrastructure scales automatically with demand.

---

## How the components fit together

```
Client (browser / curl)
        │
        │  HTTPS request
        ▼
┌─────────────────────────┐
│   Amazon API Gateway    │  REST API — routes requests to Lambda
│   (prod stage)          │
└────────────┬────────────┘
             │  Lambda Proxy Integration
             ▼
┌─────────────────────────┐
│     AWS Lambda          │  Runs handler.py — contains all route logic
│     (Python 3.13)       │
└────────────┬────────────┘
             │  JSON response
             ▼
        Client receives
        HTTP response
```

---

## Component breakdown

### Amazon API Gateway

API Gateway is the front door of the application. It:

- Exposes a public HTTPS endpoint
- Routes incoming requests to the correct backend (Lambda in this case)
- Handles TLS termination, throttling, and request/response mapping
- Is deployed to a named stage (`prod`) which forms part of the URL

Two routes are defined:

| Method | Path | Description |
|---|---|---|
| GET | /hello | Returns a greeting message |
| GET | /health | Returns a health check status |

### AWS Lambda

Lambda is the compute layer. It:

- Receives the full HTTP request as a JSON event from API Gateway
- Inspects the `path` and `httpMethod` fields to determine which route was called
- Returns a response object with `statusCode`, `headers`, and `body`
- Runs only when invoked — there is no idle cost

### IAM Execution Role

CDK automatically creates a least-privilege IAM role for the Lambda function.
This role grants Lambda permission to write logs to CloudWatch and nothing else,
following the principle of least privilege.

---

## How AWS CDK fits in

AWS CDK is the Infrastructure as Code (IaC) tool used to define and deploy
all of the above. Instead of writing raw CloudFormation YAML, CDK lets you
describe infrastructure using Python classes.

The CDK workflow is:

```
Python CDK code  →  cdk synth  →  CloudFormation template  →  cdk deploy  →  AWS resources
```

CDK constructs like `lambda_.Function` and `api_gw.LambdaRestApi` are
high-level abstractions that generate the underlying CloudFormation resources,
wire up permissions, and apply sensible defaults automatically.

---

## Why serverless?

| Concern | Traditional server | This architecture |
|---|---|---|
| Provisioning | Manual or scripted | Fully managed by AWS |
| Scaling | Configure auto-scaling | Automatic |
| Idle cost | Pay 24/7 | Pay per invocation |
| Patching | Your responsibility | AWS managed |
| Deployment | SSH / CI pipeline | `cdk deploy` |

For a simple API like this, serverless is the right default choice.
