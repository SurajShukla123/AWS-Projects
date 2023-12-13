# AWS-Projects
AWS-Projects

Project 1: EBS-Volume Cleanup

Removing EBS Volume , Which are not associated with any instance

1.  By using Lambda function and boto3 SDK with apporiate IAM role

Step 1: Write Lambda Function (Python)

Create a new Python file, e.g., cleanup_function.py.

Write the Lambda function code.

python

import boto3

def lambda_handler(event, context):
    # Define the list of specific regions
    target_regions = ['ap-south-1', 'us-east-1', 'us-east-2', 'eu-central-1']

    # Iterate through each specified region
    for region in target_regions:
        print(f"Processing region: {region}")

        # Initialize the EC2 client for the current region
        ec2_client = boto3.client('ec2', region_name=region)

        # Describe all volumes
        volumes = ec2_client.describe_volumes()['Volumes']

        # Iterate through volumes and delete unused ones
        for volume in volumes:
            # Check if the volume is not attached to any instance
            if not volume['Attachments']:
                # Delete the volume
                ec2_client.delete_volume(VolumeId=volume['VolumeId'])
                print(f"Deleted Volume: {volume['VolumeId']}")

    return {
        'statusCode': 200,
        'body': 'EBS volume cleanup complete!'
    }

This function uses the Boto3 library to interact with AWS services. It lists all volumes, checks if they are attached to any instance, and deletes the ones that are not.Step 2: 




2.Create an IAM Role for Lambd

Go to the AWS Management Console and navigate to the IAM service.

Create a new role with the "AWS Lambda" service as the trusted entity. Attach the AWSLambdaBasicExecutionRole and AmazonEC2FullAccess policies.

Step 3: Create Lambda Function

Go to the AWS Lambda service in the AWS Management Console.

Click on "Create function."

Choose "Author from scratch."

Fill in the basic information:

Name: Enter a name for your function (e.g., EbsCleanupFunction).
Runtime: Choose the Python runtime.
In the "Function code" section, upload the Python file you created (cleanup_function.py).

In the "Execution role" section, choose "Use an existing role" and select the IAM role you created.

Click on "Create function."


Step 4: Test the Lambda Function

In the Lambda function console, click on "Test."

Create a new test event and run the test. Verify that the function executes successfully.


Step 5: Create CloudWatch Events Rule  - Optional

Go to the AWS CloudWatch service in the AWS Management Console.

Click on "Rules" in the left navigation pane.

Click on "Create rule."

Choose "Event Source" as "Event Source Type" and select "Schedule."

Configure the schedule expression (e.g., rate(1 day) for daily execution).

Add a target for the rule and select the Lambda function you created.

Click on "Configure details" and give your rule a name and description.

Click on "Create rule."