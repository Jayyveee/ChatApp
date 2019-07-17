import sys
import socket
import threading
import time
import copy
import os
import math
from first import menu


class header:
    def parse_header():




class payload:



class message(header,payload):
    def gen_message(self):
        slef.soucr_ip = 
        self.desti_ip
        self.seq_no
        sock.send()
        
    def parse_message(self,recv_message): #whole msg is passed as arguement
        
    


class routing:
    def __init__(self):
        self.initial_value = math.inf
        self.rcv_buff = 4096
        self.self_id = ''
        self.dest_id = ''
        self.neighbor_nodes = {}
        self.routing_table = {}
        self.con = {}
        def route_message(gen_message,dest_ip):
            

class node:
    def __init__(self):
    self.self_info = {ip,nickname,gpg_key}
    #listening socket
     #   - one for us
     #  - one for forward.
    self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    self.sock.bind(self.ip,self.port)
    self.sock.listen()
    






#route update
