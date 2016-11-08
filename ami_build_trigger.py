import boto3
import time
def lambda_handler(event, context):
    DATEYMD = time.strftime("%Y-%m-%d")
    #DATEYMD = '2016-08-08'
    print DATEYMD
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
	    	print images['ImageId']
    
    return 'Function Complete'
