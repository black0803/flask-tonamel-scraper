def send_queue_message(msg, queue):
    if len(msg) > 5:
        return None
    queue.send_message(MessageBody=msg)
