import boto3

def main(event, context):
    # save event to logs

    sqs = boto3.resource('sqs')
    filename = f"""{event['Records'][0]['s3']['object']['key']}"""

    # change url when troubleshooting
    queueP = sqs.get_queue_by_name(QueueName='picturequeue.fifo')
    queueP.send_message (
        MessageBody = filename,
        MessageGroupId = "test"
    )

    return {
        'statusCode': 200,
        'body': event
    }
