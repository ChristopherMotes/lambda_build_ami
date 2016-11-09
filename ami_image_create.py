import boto3
import time
def lambda_handler(event, context):
    instanceID=event['detail']['instance-id']
    DATEYMD = time.strftime("%Y%m%d")
    ec2 = boto3.client('ec2')
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

    events = boto3.client('events')
    response = events.remove_targets(
        Rule='ami-auto-build',
        Ids=[ '1', ]
    )
    response = events.delete_rule(
        Name='ami-auto-build',
    )
    return 'Function Complete'
