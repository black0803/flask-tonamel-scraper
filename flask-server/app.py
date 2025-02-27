from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import os
import boto3
from botocore.exceptions import ClientError  # Import ClientError
from modules import dynamodb, sqs
import json

load_dotenv()
app = Flask(__name__)

sqs_use_ssl = os.environ.get('SQS_USE_SSL', 'True').lower() == 'true'

sqs1 = boto3.resource('sqs',
                        endpoint_url=os.getenv("SQS_ENDPOINT",None),
                        region_name=os.getenv("AWS_REGION",None),
                        # aws_secret_access_key='x',
                        # aws_access_key_id='x',
                        use_ssl=sqs_use_ssl)

dynamodb1 = boto3.resource('dynamodb',endpoint_url=os.getenv("DYNAMODB_ENDPOINT",None),
                region_name=os.getenv("AWS_REGION",None)) #, aws_access_key_id='None', aws_secret_access_key='None')
queue = None
# make sure sqs exists
try:
    queue = sqs1.get_queue_by_name(QueueName="tonamel_queue")
    print(f"Queue tonamel_queue exists.")
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
        queue = sqs1.get_queue_by_name(QueueName="tonamel_queue")
    except Exception as create_e:
        print(f"Error creating queue: {create_e}")

# make sure dynamodb exists
table = None
try:
    table = dynamodb1.Table("tonamel_events")
    table.load()
except ClientError as e:
    if e.response['Error']['Code'] == 'ResourceNotFoundException':
        try:
            table = dynamodb1.create_table(
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

@app.get("/")
def root_path():
    return render_template("index.html")

@app.post("/")
def root_submit():
    data = request.form['event_id']
    # data = modules.scraper.scrape_with_selenium("https://tonamel.com/competition/"+data+"/tournament", div_selector, os.getenv("CHROMEDRIVER","/usr/bin/chromedriver"))
    if data:
        check_event = dynamodb.get_item_by_event_id(data, table=table)
        if check_event:
            return check_event
        dynamodb.put_event_id(data, table=table)
        sqs.send_queue_message(data, queue)
        return data
    else:
        return jsonify({
            "output": "unexpected payload"
        })

@app.post("/scrape")
def scrape():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        check_event = dynamodb.get_item_by_event_id(data["event_id"], table=table)
        if check_event:
            return check_event
        try:
            dynamodb.put_event_id(data["event_id"], table=table)
            sqs.send_queue_message(data["event_id"], queue)
            return data["event_id"]
        except:
             return jsonify({
                "output": "event_id not found"
            })           
    else:
        return jsonify({
            "output": "unexpected payload"
        })

@app.post("/query-event")
def query_post():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        retrieved_item = dynamodb.get_item_by_event_id(data["event_id"])
        if retrieved_item:
            # Process the retrieved item
            data = retrieved_item.get('data') # Example: access the 'data' attribute.
            json_data = json.loads(data)
            if data:
                return json_data
        else:
            return jsonify({
                "output": "Event not found" 
            }) 
    else:
        return jsonify({
            "output": "unexpected payload"
        })

@app.get("/query-event")
def query_get():
    data = request.args.get('event_id')
    retrieved_item = dynamodb.get_item_by_event_id(data, table)
    if retrieved_item:
        # Process the retrieved item
        data = retrieved_item.get('data') # Example: access the 'data' attribute.
        json_data = json.loads(data)
        if data:
            return json_data
    else:
        return jsonify({
            "output": "Event not found" 
        }) 

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)