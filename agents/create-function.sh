#!/bin/bash
aws s3 rm s3://thousandeyes-agent/function.zip
aws s3 cp function.zip s3://thousandeyes-agent/
aws lambda delete-function --function-name AgentStatus
aws lambda create-function --debug --function-name AgentStatus --runtime python3.6 --role arn:aws:iam::633906190213:role/lambda-s3fullaceess-role --handler agent_status_lambda.lambda_handler --code S3Bucket=thousandeyes-agent,S3Key=function.zip --timeout 30 --memory-size 128
aws s3 rm s3://thousandeyes-agent/function.zip
