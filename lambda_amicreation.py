import boto3
import datetime

# Replace with your EC2 instance ID
INSTANCE_ID = 'i-00b05bc9932d7d598'

# Optional: AMI name prefix
AMI_NAME_PREFIX = 'Ec2-AMI'

# AWS region
REGION = 'us-east-1'

def lambda_handler(event, context):
    # Create EC2 client
    ec2 = boto3.client('ec2', region_name=REGION)

    # Generate AMI name with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    ami_name = f"{AMI_NAME_PREFIX}-{timestamp}"

    # Create AMI
    response = ec2.create_image(
        InstanceId=INSTANCE_ID,
        Name=ami_name,
        Description=f"AMI created from instance {INSTANCE_ID}",
        NoReboot=True  # Set False if you want a clean reboot
    )

    # Get AMI ID from response
    ami_id = response['ImageId']
    print(f"AMI created successfully! AMI ID: {ami_id}")

    # Return AMI ID
    return {
        "status": "success",
        "ami_id": ami_id,
        "ami_name": ami_name
    }