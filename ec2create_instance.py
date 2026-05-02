import boto3
client = boto3.client('ec2', region_name='us-east-1')
response = client.run_instances(
    ImageId='ami-01b14b7ad41e17ba4',
    InstanceType='t3.small',
    MaxCount=1,
    MinCount=1
)
