# Drew Schlabach
# schlabad@oregonstate.edu
# CS 361
# Assignment 5
# 11/22/25
# This program returns the number of words in a string

import zmq

def duplicate_remover(IDs):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://localhost:6437')
    input = {"list": IDs, "count": "count"}

    socket.send_json(input)
    results = socket.recv_json()

    duplicates = 0
    for duplicate in results['duplicates']:
        duplicates += 1
    
    return duplicates
