#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk_lambda_api.aws_cdk_lambda_api_stack import AwsCdkLambdaApiStack

app = cdk.App()

AwsCdkLambdaApiStack(
    app,
    "AwsCdkLambdaApiStack",
    description="Serverless Lambda-backed API built with AWS CDK in Python",
)

app.synth()
