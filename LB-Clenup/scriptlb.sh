#!/bin/bash

# Set the AWS region
region="us-east-1"

# Check if jq is available
check_jq() {
    if ! command -v jq &> /dev/null; then
        echo "jq is not installed. Download and install jq from https://stedolan.github.io/jq/download/"
        exit 1
    fi
}

# Check if AWS CLI is configured for the specified region
check_aws_config() {
    aws configure get region --output text | grep -q "$region"
    if [ $? -ne 0 ]; then
        echo "AWS CLI is not configured for the specified region ($region). Please configure AWS CLI for the correct region."
        exit 1
    fi
}

# Loop through ELBs without any listeners and with unhealthy target groups and delete them
# Print details for all Load Balancers
print_all_elbs() {
    elbs=$(aws elbv2 describe-load-balancers --region $region --output json | jq -r '.LoadBalancers')
    
    if [ -z "$elbs" ]; then
        echo "No Load Balancers found in the specified region."
        exit 0
    fi

    echo "All Load Balancers in the specified region:"
    echo "$elbs"
}
