import boto3
def lambda_handler(event, context):
    TAG_Name='test-tag'
    TAG_VPC='default'
    imageID=event['id']
    User_Data='IyEvYmluL2Jhc2gKIyMgQmFzZTY0IGVuY29kZSBtZSwgdGhlbiBhcHBseSBiYXNlNjQgb3V0cHV0IHRvIHRoZSB1c2VyIGRhdGEgc2VjdGlvbgojIyBpbnNlcnQgbm9kZSBidWlsZCBzY3JpcHQKaW5zdGFuY2VpZD1gY3VybCAtcyBjdXJsIGh0dHA6Ly8xNjkuMjU0LjE2OS4yNTQvbGF0ZXN0L21ldGEtZGF0YS9pbnN0YW5jZS1pZGAgCk5BTUU9YGF3cyAtLXJlZ2lvbiB1cy1lYXN0LTEgZWMyIGRlc2NyaWJlLXRhZ3MgLS1maWx0ZXJzICJOYW1lPXJlc291cmNlLWlkLFZhbHVlcz0kaW5zdGFuY2VpZCIgIk5hbWU9a2V5LFZhbHVlcz1OYW1lIiAtLXF1ZXJ5ICdUYWdzWzBdLlZhbHVlJyAtLW91dHB1dCB0ZXh0YCAKc3VkbyB5dW0gLXkgaW5zdGFsbCBodHRwczovL3l1bS5wdXBwZXRsYWJzLmNvbS9wdXBwZXRsYWJzLXJlbGVhc2UtcGMxLWVsLTYubm9hcmNoLnJwbQpzdWRvIHl1bSBjbGVhbiBhbGwKc3VkbyB5dW0gLXkgaW5zdGFsbCBwdXBwZXQtYWdlbnQKeXVtIC1xIC15IHVwZGF0ZQppbml0IDAK'


    ec2 = boto3.client('ec2')
    instanceDict = ec2.run_instances(
        ImageId=imageID,
        KeyName='keypair-311',
        MinCount=1,
        MaxCount=1,
        UserData=User_Data,
            InstanceType='t2.micro',
        NetworkInterfaces=[
                {
                        'DeviceIndex' : 0,
                        'SubnetId' : 'subnet-5d384f60',
                        'Groups' : [ 'sg-a886c2d2' ],
                        'AssociatePublicIpAddress': True,
                }
        ],
        IamInstanceProfile={ 'Arn': 'arn:aws:iam::742758411692:instance-profile/ami-auto-create', },
    )

    for instance in instanceDict['Instances']:
        instanceID =  instance['InstanceId']
    Event_Pattern_string="{\"source\":[\"aws.ec2\"],\"detail-type\":[\"EC2 Instance State-change Notification\"],\"detail\":{\"state\":[\"stopped\"],\"instance-id\":[ \"%s\" ]}}" % instanceID
    events=boto3.client('events')
    response = events.put_rule(
        Name='ami-auto-build',
        EventPattern=Event_Pattern_string,
        State='ENABLED',
        Description='Build AMI when triggered'
    )
    response = events.put_targets(
        Rule='ami-auto-build',
        Targets=[
            {
                'Id': '1',
                'Arn': 'arn:aws:lambda:us-east-1:742758411692:function:ami_image_create'
            },
        ]
    )
    ec2 = boto3.resource('ec2')
    response = ec2.create_tags(
        Resources=[ instanceID, ] ,
        Tags=[
                { 'Key' : 'Name', 'Value' : TAG_Name },
                { 'Key' : 'AMI_Build', 'Value' : 'True' },
        ]
    )

    return 'Image Built'
