from db_config import collection

def insert_event(event):
    collection.insert_one(event)

def get_latest_events():
    return list(collection.find().sort("timestamp", -1).limit(10))
