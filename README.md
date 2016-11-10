# lambda_build_ami
Leverages aws: cloud watch event, lambda scheduler, lambda and user data to produce a custom AMI each time aws releases a defined base ami.

# Scripts
A brief description of each of the scripts required to make the process work. The scripts are uncommented in line. I hope to cover  for the bulk of that here.
## user_data.sh
The user_data script is more of a data store. It should hold anything done on the system during customiztation.
## ami_build_trigger.py
Add this function to the lambda scheduler. Run it daily. If it sees a new verion on the describe image, ami_build_trigger, triggers the build of the AMI.
### Time variables
```
    DATEYMD = time.strftime("%Y-%m-%d")
    #DATEYMD = '2016-08-08'
```
The first variable should exit when the script is running from the scheduler. The second should be a know good time for your uncustomized AMI, uncomment when testing
### Choosing the AMI
```
    	Filters=[
    		{ 
    			'Name' : 'name',
    			'Values' : [ '*amazon-ecs-optimized' ]
```
The values line in the filter section is a glob match of the AMI provided by the vendor. In the case it's the Amazon ECS Optimized image.
### Invocation
```
        invokeResponse = lambda_client.invoke(
            FunctionName='ami_ec2_instance_create',
```
The last section is the bulk of core of the function. After we match the image we send this to another quietly waiting lambda function to start the build process.
##
## Directories
### policies
The custom prolicies added to roles used to create each required piece of the AMI. Also, you'll need to apply EC2 Read Only. Let you security and configuration management requirements deterime how your roles layout.
### function_configurations
The output from aws lambda get-function-configuration for each of the functions. Use these to help  build your functions correctly.

## Improvements
1. complex user_data stored in S3.
2. Allow  for a hash to build multi AMIs. The hash should be stored as a backend service either as a file in S3 or in dynomoDB.
