

import socket

class menu:
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    def main():
        print("****************************")
        print("!-Welcome to Chatting-!")        
        print("****************************")

        print("""enter either of the following(Press 1 - 6):
                1. One-to-one chat
                2. Group chat
                3. File Transfer
                4. View routing table
                5. List Users
                6. Exit """)

        choice = int(input("enter your choice:"))
        print("yes!")
        return choice
    
    def source_name():
        src_id = socket.gethostname()
        return src_id
    def source_port():
        src_port = 9999
        return src_port
    def node_id(self):
        n_id = gpg_key
    def destination_port(self):
        return 9999
    def destination_address(self):
        destination_address = input("Enter the destination address:")
        return destination_address
    def p_port(self):
        return "9999"
    def cost_matrix(self):
        cost = int(input("Please input link cost of the node: "))
        return cost
    def time_out(self):
        return 30
    def packet_type(self,typee):
        if typee == "data":
            return 0x02
        elif typee == "conf":
            return 0x04
        else:
            print("Error in Packet Type")
