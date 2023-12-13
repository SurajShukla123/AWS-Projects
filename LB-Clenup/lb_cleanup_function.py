import boto3
from datetime import datetime, timedelta

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

        # Describe all snapshots
        snapshots = ec2_client.describe_snapshots(OwnerIds=['self'])['Snapshots']

        # Get the current timestamp
        current_time = datetime.utcnow()

        # Iterate through snapshots and delete unused ones and those older than 30 days
        for snapshot in snapshots:
            # Check if the snapshot is not associated with any volume
            if snapshot['VolumeId'] not in [vol['VolumeId'] for vol in volumes]:
                # Check if the snapshot is older than 30 days
                snapshot_creation_time = snapshot['StartTime']
                if (current_time - snapshot_creation_time).days > 30:
                    # Delete the snapshot
                    ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                    print(f"Deleted Snapshot: {snapshot['SnapshotId']}")

    return {
        'statusCode': 200,
        'body': 'Snapshot cleanup complete!'
    }
