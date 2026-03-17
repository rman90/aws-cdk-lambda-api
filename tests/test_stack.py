import json
import pytest
import aws_cdk as cdk
from aws_cdk import assertions
from aws_cdk_lambda_api.aws_cdk_lambda_api_stack import AwsCdkLambdaApiStack


@pytest.fixture
def template():
    app = cdk.App()
    stack = AwsCdkLambdaApiStack(app, "TestStack")
    return assertions.Template.from_stack(stack)


# ── Lambda ────────────────────────────────────────────────────────────────────

def test_lambda_function_created(template):
    """Lambda function is provisioned with the correct runtime and handler."""
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Handler": "handler.handler",
            "Runtime": "python3.13",
        },
    )


def test_lambda_timeout(template):
    """Lambda timeout is set to 10 seconds."""
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {"Timeout": 10},
    )


def test_lambda_has_execution_role(template):
    """Lambda function has an IAM execution role attached."""
    template.resource_count_is("AWS::IAM::Role", 1)


# ── API Gateway ───────────────────────────────────────────────────────────────

def test_rest_api_created(template):
    """API Gateway REST API resource is created."""
    template.has_resource("AWS::ApiGateway::RestApi", {})


def test_api_deployment_created(template):
    """A single API Gateway deployment is created."""
    template.resource_count_is("AWS::ApiGateway::Deployment", 1)


def test_api_stage_is_prod(template):
    """API Gateway stage is named 'prod'."""
    template.has_resource_properties(
        "AWS::ApiGateway::Stage",
        {"StageName": "prod"},
    )


def test_hello_get_method_exists(template):
    """GET method exists on the /hello resource."""
    template.has_resource_properties(
        "AWS::ApiGateway::Method",
        {"HttpMethod": "GET"},
    )


# ── Outputs ───────────────────────────────────────────────────────────────────

def test_api_url_output_exists(template):
    """CloudFormation output for the API endpoint URL is present."""
    template.has_output("ApiEndpointUrl", {})


# ── Lambda handler unit tests ─────────────────────────────────────────────────

def make_event(path, method="GET"):
    return {"path": path, "httpMethod": method}


def test_handler_hello_route():
    """Lambda returns 200 and correct message for GET /hello."""
    from lambda.handler import handler

    response = handler(make_event("/hello"), {})
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Hello from AWS Lambda via API Gateway!"


def test_handler_health_route():
    """Lambda returns 200 and healthy status for GET /health."""
    from lambda.handler import handler

    response = handler(make_event("/health"), {})
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["status"] == "healthy"


def test_handler_unknown_route():
    """Lambda returns 404 for an unknown route."""
    from lambda.handler import handler

    response = handler(make_event("/unknown"), {})
    assert response["statusCode"] == 404
