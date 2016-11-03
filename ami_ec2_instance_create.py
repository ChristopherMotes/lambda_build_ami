import boto3

session = boto3.Session(profile_name='shaeking1')
ec2 = session.client('ec2')
instanceDict = ec2.run_instances(
	ImageId='ami-b73b63a0',
	KeyName='keypair-311',
	MinCount=1,
	MaxCount=1,
	UserData=' \
		#!/bin/bash \
		yum -y install local  https://yum.puppetlabs.com/puppetlabs-release-pc1-el-6.noarch.rpm \
		yum clean all  \
		yum -y install puppet-agent  \
	',
        InstanceType='t2.micro',
	NetworkInterfaces=[ 
		{
			'DeviceIndex' : 0,
			'SubnetId' : 'subnet-5d384f60',
        		'Groups' : [ 'sg-a886c2d2' ],
			'AssociatePublicIpAddress': True,
		}
	]
)
	
for instance in instanceDict['Instances']:
	instanceID =  instance['InstanceId']
print instanceID
