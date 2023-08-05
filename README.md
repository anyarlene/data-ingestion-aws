# AWS ETL Process with Lambda and EventBridge
This repository walks you through an automated ETL process in AWS, where we extract data from an API, and load it into an Amazon S3 bucket. The Lambda function handles the ETL, while the EventBridge schedules the Lambda execution.

## Table of Contents
- Overview
- Prerequisites
- Lambda ETL Process
- Scheduling the Lambda
- Deployment
- Conclusion

## Overview
1. Lambda ETL Process: Extract data from an external API and load it into an S3 bucket. This process also entails:

- Creating the S3 bucket (if it doesn't exist)
- Enabling server-side encryption
- Setting a lifecycle policy to transition data to Glacier after 30 days
2. EventBridge Scheduling: Automate the ETL process to run at desired intervals using AWS EventBridge.

## Prerequisites
- AWS account
- AWS CLI setup and configured with the necessary permissions
- Python's Boto3 library
- Basic understanding of Lambda, S3, and EventBridge

## Lambda ETL Process
Based on the provided code, the Lambda function follows these steps:

1. Extract
The `extract` function fetches data from an API endpoint using an API key for authentication.

2. Load
The `load` function oversees the following:

- Bucket creation (if it doesn't exist)
- Enabling server-side encryption
- Applying a lifecycle policy for transitioning data to Glacier
- Uploading the fetched data into the S3 bucket

## Scheduling the Lambda
The second script provided helps schedule the Lambda function for periodic execution. Here are the steps:

1. Initialize boto3 clients: Boto3 clients are set up for EventBridge and Lambda.

2. Define Rule and Schedule: A rule is created (or updated) in EventBridge to trigger the Lambda function. In the example, the function is triggered once every day.

3. Lambda Permission: EventBridge requires permission to trigger the Lambda function. This step grants that permission.

4. Link Rule to Lambda: The EventBridge rule is linked to the target Lambda function, completing the setup.

## Deployment
### Lambda ETL Process:
1. Use AWS Console or AWS CLI to deploy the Lambda function.
2. Assign IAM roles to the Lambda function granting permissions for S3 operations and any other AWS services you'll use.
3. Set up environment variables for the Lambda function:
    - `API_URL`: Endpoint of the data source.
    - `API_KEY`: API key for authentication with the data source.

### Lambda Scheduling:
Execute the second provided script, replacing placeholders (`<region>`, `<account_id>`, and YourLambdaFunctionName) with appropriate values to schedule the Lambda function.

## Conclusion
With this setup, the AWS ETL process becomes entirely automated, allowing data extraction from an API and loading into an S3 bucket periodically. Ensure to monitor the operations regularly and secure your resources properly, following best AWS practices.




