# Drew Schlabach
# schlabad@oregonstate.edu
# CS 361
# Assignment 5
# 11/22/25
# This program calls on the ms_check_url microservice
# to confirm the validity of a given URL.

import requests
from flask_restful.representations import json


PORT = 6015
endpoint = f'http://127.0.0.1:{PORT}/url/testUrl'

def check_url(url):
    """
    Uses the ms_url_checker microservice the test the validity of a URL.

    Returns True if URL is valid, otherwise returns False
    """
    req_obj = {"url": url}
    payload = json.dumps(req_obj)
    result = requests.post(endpoint, payload).json()

    return result['success']

