import boto3
client = boto3.client('ec2', region_name='us-east-1')
response = client.terminate_instances(
    InstanceIds=['i-04796bf43a086fc23']
)



