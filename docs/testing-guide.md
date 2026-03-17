# Testing Guide

This project includes two layers of testing: unit tests that run locally
without AWS credentials, and live endpoint validation after deployment.

---

## Unit Tests

Unit tests use `pytest` and the CDK `assertions` module to verify that the
synthesized CloudFormation template contains the expected resources.
The Lambda handler logic is also tested directly in Python.

### Run all tests

```bash
# Activate your virtual environment first
source .venv/bin/activate

pytest tests/ -v
```

### Expected output

```
tests/test_stack.py::test_lambda_function_created       PASSED
tests/test_stack.py::test_lambda_timeout                PASSED
tests/test_stack.py::test_lambda_has_execution_role     PASSED
tests/test_stack.py::test_rest_api_created              PASSED
tests/test_stack.py::test_api_deployment_created        PASSED
tests/test_stack.py::test_api_stage_is_prod             PASSED
tests/test_stack.py::test_hello_get_method_exists       PASSED
tests/test_stack.py::test_api_url_output_exists         PASSED
tests/test_stack.py::test_handler_hello_route           PASSED
tests/test_stack.py::test_handler_health_route          PASSED
tests/test_stack.py::test_handler_unknown_route         PASSED

11 passed in X.XXs
```

---

## CDK Synth Validation

`cdk synth` compiles the CDK app and validates that the stack can be
synthesized without errors. This is a fast sanity check before deploying.

```bash
cdk synth
```

Inspect the generated template:

```bash
cat cdk.out/AwsCdkLambdaApiStack.template.json | python3 -m json.tool | less
```

---

## CDK Diff

Before redeploying after a change, use `cdk diff` to preview exactly what
will be added, modified, or removed:

```bash
cdk diff
```

---

## Live Endpoint Testing

After a successful `cdk deploy`, test the live API using `curl`.

```bash
BASE_URL="https://<your-api-id>.execute-api.<region>.amazonaws.com/prod"

# Test /hello
curl -s "$BASE_URL/hello" | python3 -m json.tool
```

Expected response:
```json
{
    "message": "Hello from AWS Lambda via API Gateway!"
}
```

```bash
# Test /health
curl -s "$BASE_URL/health" | python3 -m json.tool
```

Expected response:
```json
{
    "status": "healthy"
}
```

```bash
# Test 404 handling
curl -s "$BASE_URL/unknown" | python3 -m json.tool
```

Expected response:
```json
{
    "error": "Route GET /unknown not found"
}
```

---

## Checking Lambda Logs

View real-time Lambda logs using the AWS CLI:

```bash
aws logs tail /aws/lambda/AwsCdkLambdaApiStack-ApiHandler --follow
```

Or use the CDK watch command to stream logs during development:

```bash
cdk watch
```
