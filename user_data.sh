#!/bin/bash
## Base64 encode me, then apply base64 output to the user data section
## insert node build script
instanceid=`curl -s curl http://169.254.169.254/latest/meta-data/instance-id` 
NAME=`aws --region us-east-1 ec2 describe-tags --filters "Name=resource-id,Values=$instanceid" "Name=key,Values=Name" --query 'Tags[0].Value' --output text` 
sudo yum -y install https://yum.puppetlabs.com/puppetlabs-release-pc1-el-6.noarch.rpm
sudo yum clean all
sudo yum -y install puppet-agent
yum -q -y update
init 0
