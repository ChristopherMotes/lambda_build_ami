import boto3

ec2 = boto3.resource('ec2')
image = ec2.Image('id')
