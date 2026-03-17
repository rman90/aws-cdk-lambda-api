# 🚀 AWS CDK Lambda API

A serverless REST API built with **AWS CDK in Python**, demonstrating how to
define, deploy, test, and update cloud infrastructure using Infrastructure as Code.

**Author:** Ross Nesbitt
**GitHub:** [github.com/rman90](https://github.com/rman90)

---

## 📋 Overview

This project provisions a fully serverless API on AWS using:

- **Amazon API Gateway** — public HTTPS endpoint
- **AWS Lambda** — Python function that handles requests
- **AWS CDK (Python)** — defines and deploys all infrastructure as code

The API exposes two routes:

| Method | Route | Response |
|---|---|---|
| GET | `/hello` | `{"message": "Hello from AWS Lambda via API Gateway!"}` |
| GET | `/health` | `{"status": "healthy"}` |

No servers. No manual console clicks. One command to deploy everything.

---

## 🎯 Objectives

This project demonstrates how to:

- ✅ Build AWS infrastructure using Python CDK constructs
- ✅ Define a CDK application using the AWS Construct Library
- ✅ Deploy an AWS CDK application to a live AWS environment
- ✅ Validate infrastructure correctness with unit tests
- ✅ Update infrastructure and redeploy changes safely

---

## 🏗️ Architecture

```
Client (browser / curl)
        │
        │  HTTPS
        ▼
┌─────────────────────────┐
│   Amazon API Gateway    │
│      (prod stage)       │
└────────────┬────────────┘
             │  Lambda Proxy Integration
             ▼
┌─────────────────────────┐
│      AWS Lambda         │
│     (Python 3.13)       │
└────────────┬────────────┘
             │
             ▼
      JSON Response
```

AWS CDK synthesizes this architecture into a CloudFormation template and
deploys it to your AWS account with a single command.

---

## 📁 Project Structure

```
aws-cdk-lambda-api/
│
├── README.md                          # You are here
├── app.py                             # CDK app entry point
├── cdk.json                           # CDK configuration
├── requirements.txt                   # Python dependencies
├── source.bat                         # Windows venv activation helper
├── .gitignore
│
├── aws_cdk_lambda_api/
│   ├── __init__.py
│   └── aws_cdk_lambda_api_stack.py    # CDK stack — all infrastructure defined here
│
├── lambda/
│   └── handler.py                     # Lambda function code
│
├── tests/
│   └── test_stack.py                  # Unit tests (CDK assertions + handler logic)
│
├── docs/
│   ├── deployment-guide.md            # Step-by-step deployment instructions
│   ├── testing-guide.md               # How to run and interpret tests
│   └── architecture-explanation.md   # Deep dive into the architecture
│
└── diagrams/
    └── architecture-diagram.txt       # Architecture diagram reference
```

---

## ✅ Prerequisites

Make sure the following are installed and configured before you begin:

| Tool | Purpose | Install |
|---|---|---|
| Python 3.11+ | CDK app and Lambda runtime | [python.org](https://www.python.org) |
| Node.js 18+ | Required by CDK CLI | [nodejs.org](https://nodejs.org) |
| AWS CDK CLI | Deploy infrastructure | `npm install -g aws-cdk` |
| AWS CLI | Interact with AWS | [docs.aws.amazon.com/cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) |
| AWS credentials | Authenticate to AWS | `aws configure` |

Verify everything is ready:

```bash
python3 --version
node --version
cdk --version
aws sts get-caller-identity
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/rman90/aws-cdk-lambda-api.git
cd aws-cdk-lambda-api
```

### 2. Create and activate a virtual environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
source.bat
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Bootstrap your AWS environment

> Only required once per AWS account/region combination.

```bash
cdk bootstrap
```

### 5. Synthesize the CloudFormation template

Compiles your CDK code into CloudFormation without deploying anything.
Use this to inspect what will be created.

```bash
cdk synth
```

### 6. Deploy the stack

```bash
cdk deploy
```

On success, the API endpoint URL is printed in the terminal:

```
Outputs:
AwsCdkLambdaApiStack.ApiEndpointUrl = https://abc123.execute-api.us-east-1.amazonaws.com/prod/
```

---

## 🧪 Testing

### Run unit tests

```bash
pytest tests/ -v
```

Tests cover:

- Lambda function is created with the correct runtime and handler
- Lambda timeout is configured
- IAM execution role exists
- API Gateway REST API is created
- API stage is named `prod`
- GET method exists on `/hello`
- CloudFormation output for the API URL is present
- Lambda handler returns correct responses for all routes

### Validate the live API

```bash
BASE_URL="https://<your-api-id>.execute-api.<region>.amazonaws.com/prod"

curl "$BASE_URL/hello"
# {"message": "Hello from AWS Lambda via API Gateway!"}

curl "$BASE_URL/health"
# {"status": "healthy"}
```

See [docs/testing-guide.md](docs/testing-guide.md) for the full testing reference.

---

## 🔄 Updating the Application

One of the key benefits of CDK is how easy it is to update infrastructure.

### Example: change the Lambda response message

Edit `lambda/handler.py`:

```python
# Before
"body": json.dumps({"message": "Hello from AWS Lambda via API Gateway!"}),

# After
"body": json.dumps({"message": "Hello from AWS Lambda — updated response!"}),
```

Preview the change:

```bash
cdk diff
```

Deploy the update:

```bash
cdk deploy
```

CDK detects only the Lambda code changed and updates just that resource.
Verify the change:

```bash
curl "$BASE_URL/hello"
# {"message": "Hello from AWS Lambda — updated response!"}
```

### Example: add a new route

In `aws_cdk_lambda_api/aws_cdk_lambda_api_stack.py`, add a new resource:

```python
info_resource = api.root.add_resource("info")
info_resource.add_method("GET")
```

In `lambda/handler.py`, add the handler logic:

```python
if path == "/info" and http_method == "GET":
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"project": "aws-cdk-lambda-api", "version": "1.1.0"}),
    }
```

Then redeploy:

```bash
cdk deploy
```

---

## 🧹 Cleanup

To remove all AWS resources created by this project and avoid ongoing charges:

```bash
cdk destroy
```

---

## 💡 Skills Demonstrated

| Skill | How it's shown |
|---|---|
| **AWS CDK** | Full stack defined in Python using CDK constructs |
| **Infrastructure as Code** | All resources version-controlled, repeatable, and reviewable |
| **Python development** | Clean, readable Lambda and CDK code |
| **Serverless architecture** | Lambda + API Gateway — no servers to manage |
| **API Gateway integration** | REST API with explicit routes and Lambda proxy integration |
| **Lambda deployment** | Function packaged and deployed via CDK assets |
| **IAM best practices** | Least-privilege execution role auto-generated by CDK |
| **Testing & validation** | CDK assertions, handler unit tests, and live curl validation |
| **CloudFormation outputs** | API URL surfaced as a stack output |

---

## 📚 Further Reading

- [AWS CDK Developer Guide](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
- [AWS CDK Python Reference](https://docs.aws.amazon.com/cdk/api/v2/python/)
- [Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)

---

## 🪞 Lessons Learned

Building this project reinforced several important concepts:

- **CDK abstractions save time** — `LambdaRestApi` wires up the Lambda integration,
  permissions, and deployment in a few lines of code that would take hundreds of
  lines of raw CloudFormation.
- **Synth before deploy** — running `cdk synth` catches errors early without
  touching AWS resources.
- **CDK diff is underrated** — seeing exactly what will change before deploying
  builds confidence and prevents surprises in production.
- **Unit tests for IaC matter** — testing the synthesized template means you can
  catch infrastructure regressions the same way you catch code bugs.
- **Least privilege by default** — CDK's auto-generated IAM roles follow security
  best practices out of the box, which is a good habit to carry into larger projects.

---

*Built with ☁️ and Python by [Ross Nesbitt](https://github.com/rman90)*
