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

### Notes
1. This takes a long time run in lambda terms, 15-30 seconds. Plan your spending accordingly.
2. Runing the script daily, keeps the date comparison brief. If I change this, it will be a monthly run.
3. lambda means something to python. So all of my boto3 lambda clients are named lambda_client and not just lambda. And absolutely not the non-self documenting client that the boto3 docs use.

## ami_ec2_instance_create.py
This builds the ec2 instance and adds the cloudwatch event (see notes for this section).

### Variables
1. The TAGs variables are cruft from the previous project that was the source for hacking this script. 
1. `imageID=event['id']` is a lambda thingy. I won't over explain.
1. User_Data is set as a variable data because it's easier to update. The value is a base64 encoding of you user_data.sh script.

### Run Instances
`instanceDict = ec2.run_instances(` is fairly straight foreward. Of course, salt to taste.

### Put Rule and Put Targets
You have to put a rule then a target. The rule ami-auto-build waits for the instance to goto a stopped state. The target calls the last lambda function (See Notes for this section)

### Tagging
The last section just adds tags to the instance. Use tags!

### Notes
1. I had very good reason for creating an event instead of invoking the ami_image_create lambda function from the user data. I can't figure it out now, but it was real and it was spactacular. 

## ami_image_create.py
This script is the last lambda function. We take our image we built and turn it into an AMI. Then we delete the now, unneeded, cloudwatch events.
### Variables
`instanceID=event['detail']['instance-id']` Lookie, deep hashing on a lambda thingie

### Create Image
```
    Name_string = "test-ami-%s" % DATEYMD
    response = ec2.create_image(
        InstanceId=instanceID,
        Name=Name_string,
```
Create image is fairly straight forward read aws and boto3 documentation for questions

### Remove Tagets and rule
```
    events = boto3.client('events')
    response = events.remove_targets(
<snip>
    response = events.delete_rule(
```
Here we clean up the cloud watch events. Since we add them automagically when we needd them, there's no reason to leave them hanging around.

### 
## Directories
### policies
The custom prolicies added to roles used to create each required piece of the AMI. Also, you'll need to apply EC2 Read Only. Let you security and configuration management requirements deterime how your roles layout.
### function_configurations
The output from aws lambda get-function-configuration for each of the functions. Use these to help  build your functions correctly.

## Improvements
1. complex user_data stored in S3.
2. Allow  for a hash to build multi AMIs. The hash should be stored as a backend service either as a file in S3 or in dynomoDB.
