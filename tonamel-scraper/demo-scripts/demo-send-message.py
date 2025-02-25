from dotenv import load_dotenv
import boto3
import os

load_dotenv()
# data = modules.scraper.scrape_with_selenium("https://tonamel.com/competition/YaSgI/tournament", "matchup-card__inner", os.getenv("CHROMEDRIVER","/usr/bin/chromedriver"))
# print(data)

sqs = boto3.resource('sqs',
                        endpoint_url=os.getenv("SQS_ENDPOINT","http://localhost:9324"),
                        region_name='elasticmq',
                        # aws_secret_access_key='x',
                        # aws_access_key_id='x',
                        use_ssl=False)

queue = sqs.get_queue_by_name(QueueName='tonamel_queue')

msg=os.getenv("EVENT_ID","") 
print(len(msg))
queue.send_message(MessageBody=msg)
