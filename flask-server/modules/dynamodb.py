def get_item_by_event_id(event_id, table):
    if len(event_id) > 5:
        return None
    try:
        response = table.get_item(Key={'event_id': event_id})  # Use 'event_id'
        item = response.get('Item')  # Extract the item from the response

        if item:
            print(f"item '{event_id}' found")
            return item  # Return the item if found
        else:
            print(f"Item with event_id '{event_id}' not found.")
            return None  # Return None if not found

    except Exception as e:
        print(f"Error querying DynamoDB: {e}")
        return None  # Return None on error
    
def put_event_id(event_id, table):
    if len(event_id) > 5:
        return None
    table.put_item(Item={'event_id': event_id, 'data': {'status':'pending'}})
    return {'event_id': event_id, 'data': {'status':'pending'}}