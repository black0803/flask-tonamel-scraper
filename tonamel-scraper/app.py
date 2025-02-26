import modules.scraper
from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError  # Import ClientError

load_dotenv()
# initialize boto3 resources
sqs = boto3.resource('sqs',
                        endpoint_url=os.getenv("SQS_ENDPOINT","http://localhost:9324"),
                        region_name='elasticmq',
                        # aws_secret_access_key='x',
                        # aws_access_key_id='x',
                        use_ssl=False)

dynamodb = boto3.resource('dynamodb',endpoint_url=os.getenv("DYNAMODB_ENDPOINT","http://localhost:8000"),
                region_name='None') #, aws_access_key_id='None', aws_secret_access_key='None')

queue = None
# make sure sqs exists
try:
    queue = sqs.get_queue_by_name(QueueName="tonamel_queue")
    print(f"Queue tonamel_queue exists.")
# except ClientError as e:
#     if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue': # Correct exception name
except ClientError as e:  # Catch ClientError
    print(f"Queue tonamel_queue does not exist.")
    try:
        sqs_client = boto3.client('sqs',  # Create a client *just* for queue creation
                                endpoint_url=os.getenv("SQS_ENDPOINT","http://localhost:9324"),
                                region_name='elasticmq',
                                # aws_secret_access_key='x',
                                # aws_access_key_id='x',
                                use_ssl=False)
        create_response = sqs_client.create_queue(QueueName="tonamel_queue")
        new_queue_url = create_response['QueueUrl']
        print(f"Queue tonamel_queue created. URL: {new_queue_url}")
        queue_url = new_queue_url  # Update queue_url
        queue = sqs.get_queue_by_name(QueueName="tonamel_queue")
    except Exception as create_e:
        print(f"Error creating queue: {create_e}")

# make sure dynamodb exists
try:
    table = dynamodb.Table("tonamel_events")
    table.load()
except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        try:
            table = dynamodb.create_table(
                TableName = "tonamel_events",
                KeySchema = [
                    {
                        'AttributeName': 'event_id',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions = [
                    {
                        'AttributeName': 'event_id',
                        'AttributeType': 'S'  # String type
                    },
                ],
                ProvisionedThroughput={  # This is where you set it!
                    'ReadCapacityUnits': 5,  # Adjust these based on your needs
                    'WriteCapacityUnits': 5   # Adjust these based on your needs
                }
            )
            table.wait_until_exists()
            print(f"Table tonamel_events created.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # main program
    if queue:
        while(True):
            for message in queue.receive_messages():
                event_id = message.body
                if len(event_id) > 5:
                    table.delete_item(Item={'event_id': event_id})
                    message.delete()
                    continue
                data = modules.scraper.scrape_with_selenium("https://tonamel.com/competition/"+event_id+"/tournament", "matchup-card__inner", os.getenv("CHROMEDRIVER","/usr/bin/chromedriver"))
                print(data)
                if data:
                    table.put_item(Item={'event_id': event_id, 'data': str(data)})
                else:
                    table.delete_item(Item={'event_id': event_id})
                message.delete()
 