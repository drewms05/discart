# Drew Schlabach
# schlabad@oregonstate.edu
# CS 361
# Assignment 5
# 11/22/25
# This program returns the number of words in a string

import zmq

def word_counter(phrase):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://localhost:9875')
    socket.send_string(phrase)
    results = socket.recv_string()
    return results
