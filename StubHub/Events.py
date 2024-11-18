import requests

def get_event_details(url):
    return requests.post(url).json()