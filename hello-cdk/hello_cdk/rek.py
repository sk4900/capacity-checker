import boto3

def detect_labels(photo, bucket):
    # returns number of people detected in image
    client=boto3.client('rekognition')
    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
        MaxLabels=5)
    sum = 0
    for label in response['Labels']:
        if (label['Name'] == 'Person'):
            for instance in label['Instances']:
                sum += 1
    return sum
    
def send_message(count, photo, queueName):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=queueName)
    response = queue.send_message(
        MessageBody=photo,
        MessageAttributes={
            'Count': {
                'StringValue': count,
                'DataType': 'String'
            }
        }
    )
    return response
def main():

    label_count=detect_labels(photo, bucket)
    print("People detected: " + str(label_count))


if __name__ == "__main__":
    main()