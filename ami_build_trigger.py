import boto3

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
	]
)

 
for printer in imagesDict:
	print printer

