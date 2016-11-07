#!/bin/bash
## Base64 encode me, then apply base64 output to the user data section
instanceid=`curl -s curl http://169.254.169.254/latest/meta-data/instance-id` 
NAME=`aws --region us-east-1 ec2 describe-tags --filters "Name=resource-id,Values=$instanceid" "Name=key,Values=Name" --query 'Tags[0].Value' --output text` 
