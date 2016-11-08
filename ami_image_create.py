import boto3
import time
instanceID='i-00e93862323dd6d88'
DATEYMD = time.strftime("%Y%m%d")
session = boto3.Session(profile_name='shaeking1')
ec2 = session.client('ec2')
Name_string = "test-ami-%s" % DATEYMD
response = ec2.create_image(
	InstanceId=instanceID,
	Name=Name_string,
	Description='Test of ami autobuild',
	NoReboot=False
)
response = ec2.terminate_instances(
	InstanceIds=[ instanceID, ]
	
)

events = session.client('events')
response = events.delete_rule(
	Name='ami-auto-build',
)
