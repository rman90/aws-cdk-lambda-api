import os

from aws_cdk import (
    CfnOutput,
    Duration,
    Stack,
    aws_apigateway as api_gw,
    aws_lambda as lambda_,
)
from constructs import Construct


class AwsCdkLambdaApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda function
        api_handler = lambda_.Function(
            self,
            "ApiHandler",
            runtime=lambda_.Runtime.PYTHON_3_13,
            handler="handler.handler",
            code=lambda_.Code.from_asset(os.path.join(os.path.dirname(__file__), "..", "lambda")),
            timeout=Duration.seconds(10),
            description="Handles API Gateway requests for the hello and health routes",
        )

        # REST API backed by the Lambda function
        # proxy=True forwards all routes and methods to the Lambda
        api = api_gw.LambdaRestApi(
            self,
            "HelloApi",
            handler=api_handler,
            proxy=False,
            description="Serverless REST API powered by AWS Lambda",
            deploy_options=api_gw.StageOptions(stage_name="prod"),
        )

        # GET /hello
        hello_resource = api.root.add_resource("hello")
        hello_resource.add_method("GET")

        # GET /health
        health_resource = api.root.add_resource("health")
        health_resource.add_method("GET")

        # Output the API endpoint URL
        CfnOutput(
            self,
            "ApiEndpointUrl",
            value=api.url,
            description="Base URL of the deployed API Gateway endpoint",
        )
