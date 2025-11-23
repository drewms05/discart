# Drew Schlabach
# schlabad@oregonstate.edu
# CS 361
# Assignment 5
# 11/3/25
# This program validates a given string

import zmq

def string_validator(username):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://localhost:5454')
    input = {'input': username, 'min': '3', 'max': '20'}

    socket.send_json(input)
    results = socket.recv_json()

    if results[0] == 'String is not valid':
        return False