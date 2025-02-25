import modules.scraper
import os
from dotenv import load_dotenv
import boto3
import json

load_dotenv()
# data = modules.scraper.scrape_with_selenium("https://tonamel.com/competition/YaSgI/tournament", "matchup-card__inner", os.getenv("CHROMEDRIVER","/usr/bin/chromedriver"))
# print(data)

dynamodb = boto3.resource('dynamodb',endpoint_url='http://192.168.1.101:8000',
                region_name='None', aws_access_key_id='None', aws_secret_access_key='None')
table = dynamodb.Table("tonamel_events")

def get_item_by_event_id(event_id):
    try:
        response = table.get_item(Key={'event_id': event_id})  # Use 'event_id'
        item = response.get('Item')  # Extract the item from the response

        if item:
            print(f"Item found:")
            return item  # Return the item if found
        else:
            print(f"Item with event_id '{event_id}' not found.")
            return None  # Return None if not found

    except Exception as e:
        print(f"Error querying DynamoDB: {e}")
        return None  # Return None on error

# Example usage:
event_id_to_query = 'dco5a'  # Replace with the event_id you want to query
retrieved_item = get_item_by_event_id(event_id_to_query)

if retrieved_item:
    # Process the retrieved item
    data = retrieved_item.get('data') # Example: access the 'data' attribute.
    json_data = json.loads(data)
    if data:
        print(json_data)
        # print(type(json_data))
    # ... other processing ...

else:
    print("Could not retrieve the item.")