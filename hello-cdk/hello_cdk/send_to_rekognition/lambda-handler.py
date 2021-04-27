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

def send_to_fifo(count, fileName, queueName):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=queueName)
    response = queue.send_message(
        MessageBody=fileName,
        MessageGroupId = "counts",
        MessageAttributes={
            'Count': {
                'StringValue': str(count),
                'DataType': 'String'
            }
        }
    )
    return response
      
def main(event, context):
    # save event to logs

    filename = f"""{event['Records'][0]['body']}"""

    s3_client = boto3.client('s3')

    #destination_bucket_name = 'bucketswen614'

    # Bucket Name where file was uploaded
    source_bucket_name = 'bucketswen614'
    # Copy Source Object
    #copy_source_object = {'Bucket': source_bucket_name, 'Key': filename}

    # S3 copy object operation
    #s3_client.copy_object(CopySource=copy_source_object, Bucket=destination_bucket_name, Key=filename)


    # Send to DB FIFO Queue
    send_to_fifo(detect_labels(filename, source_bucket_name), filename, 'dbqueue.fifo')
    
    s3_client.delete_object(Bucket=source_bucket_name, Key=filename)

    return {
        'statusCode': 200,
        'body': event
    }