import boto3
sns = boto3.client('sns')
number = '+14089214831'
sns.publish(PhoneNumber = number, Message='example text message' )