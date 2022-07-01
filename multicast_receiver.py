# MULTICAST https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python
import pickle
import socket
import struct

import multicast_data
import server
import server_data

#global multicast_data
multicastIP= multicast_data.MCAST_GRP

serverAddress = ('',multicast_data.MCAST_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def pickle_load_reader(data,pos):
    return pickle.loads(data)[pos]