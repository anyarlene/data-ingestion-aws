import boto3

def schedule_lambda_function(lambda_function_name):
    # Initialize boto3 clients for EventBridge (formerly CloudWatch Events) and Lambda
    events_client = boto3.client('events')
    lambda_client = boto3.client('lambda')

    # Define rule name and schedule expression
    rule_name = "DailyLambdaTrigger"
    schedule_expression = "rate(1 day)"

    # Create or update CloudWatch Events rule
    response = events_client.put_rule(
        Name=rule_name,
        ScheduleExpression=schedule_expression,
        State='ENABLED'
    )
    rule_arn = response['RuleArn']

    # Add permission for the EventBridge (CloudWatch Events) rule to invoke the Lambda function
    lambda_client.add_permission(
        FunctionName=lambda_function_name,
        StatementId=f"{rule_name}-event",
        Action='lambda:InvokeFunction',
        Principal='events.amazonaws.com',
        SourceArn=rule_arn
    )

    # Link the rule to the target Lambda function
    events_client.put_targets(
        Rule=rule_name,
        Targets=[
            {
                'Id': '1',
                'Arn': f"arn:aws:lambda:<region>:<account_id>:function:{lambda_function_name}"  # Replace <region> and <account_id> with appropriate values
            }
        ]
    )

    print(f"Successfully scheduled {lambda_function_name} to be triggered by {rule_name}.")

if __name__ == '__main__':
    lambda_function_name = "YourLambdaFunctionName"  # Replace with your Lambda function name
    schedule_lambda_function(lambda_function_name)
