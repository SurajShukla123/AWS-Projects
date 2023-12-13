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
