import boto3
import time

DATEYMD = time.strftime("%Y-%m-%d")
#DATEYMD = '2016-08-08'
print DATEYMD
session = boto3.Session(profile_name='shaeking1')
ec2 = session.client('ec2')
imagesDict = ec2.describe_images(
	Owners=[
		'amazon',
	],
	Filters=[
		{ 
			'Name' : 'name',
			'Values' : [
				'*amazon-ecs-optimized'
			]
		},
		{
			'Name' : 'state',
			'Values' : [
				'pending',
				'available'
			]
		}
	]
)
 
for images in imagesDict['Images'] :
	if DATEYMD in images['CreationDate']:
		print images['ImageId']

