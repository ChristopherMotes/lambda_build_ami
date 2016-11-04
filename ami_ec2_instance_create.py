import boto3

TAG_Name='test-tag'
TAG_VPC='default'


session = boto3.Session(profile_name='shaeking1')
ec2 = session.client('ec2')
instanceDict = ec2.run_instances(
	ImageId='ami-b73b63a0',
	KeyName='keypair-311',
	MinCount=1,
	MaxCount=1,
	UserData='IyEvYmluL2Jhc2gNCnl1bSAteSBpbnN0YWxsIGh0dHBzOi8veXVtLnB1cHBldGxhYnMuY29tL3B1cHBldGxhYnMtcmVsZWFzZS1wYzEtZWwtNi5ub2FyY2gucnBtDQp5dW0gY2xlYW4gYWxsDQp5dW0gLXkgaW5zdGFsbCBwdXBwZXQtYWdlbnQNCi9vcHQvcHVwcGV0bGFicy9iaW4vcHVwcGV0IHJlc291cmNlIGhvc3QgcHVwcGV0Lm1haW50Lm1vdGVzIGVuc3VyZT1wcmVzZW50IGlwPTE5Mi4xNjguMC41MCBob3N0X2FsaWFzZXM9cHVwcGV0DQppbnN0YW5jZWlkPWBjdXJsIC1zIGN1cmwgaHR0cDovLzE2OS4yNTQuMTY5LjI1NC9sYXRlc3QvbWV0YS1kYXRhL2luc3RhbmNlLWlkYCANCk5BTUU9YGF3cyAtLXJlZ2lvbiB1cy1lYXN0LTEgZWMyIGRlc2NyaWJlLXRhZ3MgLS1maWx0ZXJzICJOYW1lPXJlc291cmNlLWlkLFZhbHVlcz0kaW5zdGFuY2VpZCIgIk5hbWU9a2V5LFZhbHVlcz1OYW1lIiAtLXF1ZXJ5ICdUYWdzWzBdLlZhbHVlJyAtLW91dHB1dCB0ZXh0YCANClZQQz1gYXdzIC0tcmVnaW9uIHVzLWVhc3QtMSBlYzIgZGVzY3JpYmUtdGFncyAtLWZpbHRlcnMgIk5hbWU9cmVzb3VyY2UtaWQsVmFsdWVzPSRpbnN0YW5jZWlkIiAiTmFtZT1rZXksVmFsdWVzPVZQQyIgLS1xdWVyeSAnVGFnc1swXS5WYWx1ZScgLS1vdXRwdXQgdGV4dGAgDQplY2hvICJUaGlzIGlzIGEgdGVzdCBmb3IgJE5BTUUiID4gL3RtcC9maWxlIGVjaG8gIlRoaXMgaXMgYSB0ZXN0IGZvciAkVlBDIiA+PiAvdG1wL2ZpbGU=',
        InstanceType='t2.micro',
	NetworkInterfaces=[ 
		{
			'DeviceIndex' : 0,
			'SubnetId' : 'subnet-5d384f60',
        		'Groups' : [ 'sg-a886c2d2' ],
			'AssociatePublicIpAddress': True,
		}
	],
	IamInstanceProfile={ 'Arn': 'arn:aws:iam::742758411692:instance-profile/new-test-role', },
)
	
for instance in instanceDict['Instances']:
	instanceID =  instance['InstanceId']

ec2 = session.resource('ec2')
response = ec2.create_tags( 
	Resources=[ instanceID, ] ,
	Tags=[
		{ 'Key' : 'Name', 'Value' : TAG_Name },
		{ 'Key' : 'VPC', 'Value': TAG_VPC }
	]
)

