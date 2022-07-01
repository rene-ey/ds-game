import pickle
import socket
import sys

import heartbeat
import leader_election
import multicast_data
import multicast_receiver
import multicast_sender
import ports
import server_data
import logging
from time import sleep

import thread_helper

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s:%(name)s:%(message)s')


def send_leader():
    if multicast_data.LEADER == server_data.SERVER_IP and len(multicast_data.SERVER_LIST) > 0:
        for i in range(len(multicast_data.SERVER_LIST)):
            replica = multicast_data.SERVER_LIST[i]
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            try:
                sock.connect((replica, ports.LEADER_NOTIFICATION_PORT))
                leader_message = pickle.dumps(multicast_data.LEADER)
                sock.send(leader_message)
                logging.info(f'Leader {multicast_data.LEADER} is updating the leader parameter fpr {replica}')
                print(f'Updating Leader for {replica}')
            except:
                logging.critical(f'Failed to update leader address for {replica}')
                print(f'Failed to send Leader address to {replica}')
            finally:
                sock.close()

# listener to receiver Leader information for replica server
def receive_leader():
    server_address = ('', ports.LEADER_NOTIFICATION_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen()

    while True:
        connection, leader_address = sock.accept()
        leader = pickle.loads(connection.recv(1024))

        multicast_data.LEADER = leader
        print(f'LEADER IS: {multicast_data.LEADER}')

# sends server List to replica servers over TCP
def send_server_list():
    if multicast_data.LEADER == server_data.SERVER_IP and len(multicast_data.SERVER_LIST ) > 0:
        for i in range(len(multicast_data.SERVER_LIST)):
            if multicast_data.SERVER_LIST[i] != server_data.SERVER_IP:
                replica = multicast_data.SERVER_LIST[i]
                ip = replica
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sleep(1)
                try:
                    sock.connect((ip,ports.SERVERLIST_UPDATE_PORT))
                    
                    updated_list = pickle.dumps(multicast_data.SERVER_LIST)
                    sock.send(updated_list)
                    logging.info(f'Updating Server List for {ip}')
                    print(f'Updating Server List for {ip}')
                except:
                    logging.critical(f'failed to send serverlist {ip}')
                    print(f'failed to send serverlist {ip}')
                finally:
                    sock.close()

# listener to receive server list from leader over TCP
def receive_server_list():
    server_address = ('', ports.SERVERLIST_UPDATE_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    sock.listen()

