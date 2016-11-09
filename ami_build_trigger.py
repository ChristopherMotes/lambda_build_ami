import boto3
import time
def lambda_handler(event, context):
    DATEYMD = time.strftime("%Y-%m-%d")
    #DATEYMD = '2016-08-08'
    imageID=None
    ec2 = boto3.client('ec2')
    imagesDict = ec2.describe_images(
    	Owners=[
    		'amazon',
    	],
    	Filters=[
    		{ 
    			'Name' : 'name',
    			'Values' : [ '*amazon-ecs-optimized' ]
    		},
    		{
    			'Name' : 'state',
    			'Values' : [
	    			'pending',
		    		'available'
			    ]
    		},
    		{
	    		'Name' : 'image-type',
		    	'Values' : [ 'machine' ]
		    }
	    ]
    )
 
    for images in imagesDict['Images'] :
    	if DATEYMD in images['CreationDate']:
	    	imageID = images['ImageId']
    
    lambda_client = boto3.client('lambda')
    if imageID is not None:
    	print imageID
        invokeResponse = lambda_client.invoke(
            FunctionName='ami_ec2_instance_create',
            InvocationType='Event',
            LogType='Tail',
            Payload='{"id":"'+ imageID +'"}'
        )
        print invokeResponse
    
    return 'Function Complete'
