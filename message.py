import sys
import socket
import binascii
import json
import threading
import random
import time


"""packet header"""
header_len = 20

class packet_header:
   udp_data = bytes()
   dest = bytes()
   source = bytes()
   version = 0
   packet_type = 0
   flags = 0
   session = 0
   sequence = 0

   #definite variables to be called 

def __init__(self,udp_data,dest,source,version,packet_type,flags,session,sequence):
    self.udp_data = udp_data
    self.dest = dest 
    self.source = source 
    self.version = version
    self.packet_type = packet_type
    self.flags = flags
    self.session = session 
    self.sequence = sequence
    
    #message
    def packet(self,udp_data):

        if (len(udp_data) >= header_len):
            byte0 = int.from_bytes(udp_data[0:1], byteorder = "big")
            dest = udp_data[9:17]
            source = udp_data[1:9]
            sequence = int.from_bytes(udp_data[18:20], byteorder = 'big')
            version = ((byte0 & 0xC0) >> 6)
            packet_type = ((byte0 & 0x38) >> 3)
            flags = (byte0 & 0x07)
            session = int.from_bytes(udp_data[17:18], byteorder='big')
            length = int.from_bytes(udp_data[9:10], byteorder='big')
            payload = udp_data[20:]
            
            return packet_header(packet_type, flags, source, dest, session, sequence, payload)

        else:

            raise Exception("Packet is not up to the required length:", len(udp_data))
        
        #encoding
    def encode(self):
        byte = bytearray()
        byte.append((self.version << 6) | (self.packet_type << 3)| self.flags)
        byte.extend(self.udp_data)
        byte.extend(self.session.to_bytes(1, byteorder = 'big'))
        byte.extend(self.source)
        byte.extend(self.dest)
        byte.extend(self.sequence.to_bytes(2, byteorder = 'big'))

        return bytes(byte)


    def  __str__(self):
        return "version: " + hex(self.version) + "\n" + \
            "type: " + hex(self.packet_type) + "\n" + \
                "flags: " + hex(self.flags) + "\n" + \
                    + "session: " + hex(self.session) + "\n" + \
                        + "sequence: " + hex(self.sequence) + "\n" + \
                            "source: " + print_hex(self.source) + "\n" + \
                                + "destination: " + print_hex(self.dest) + "\n" + \
                                    + "udp_data: " + print_hex(self.udp_data) + "\n"

    
    def ack(self):
        return packet_header(self.packet_type, 0x04, self.source, self.dest,self.session,self.sequence,bytes())
    

class segmentation:
    packet_type = 0
    destination = bytes()
    udp_data = bytes()
    session = 0
    source = bytes()


    def __init__(self, packet_type, source, dest, session, udp_data):
        self.session = session
        self.packet_type = packet_type
        self.source = source
        self.dest = dest
        self.udp_data = udp_data
    

    def init_assemble(self, packets):
        
        first_packets = self.find_packet_with_flags(self, 0x03, packets)
        second_packets = self.find_packet_with_flags(self, 0x01, packets)
        last_packets = self.find_packet_with_flags(self, 0x02, packets)
        if (first_packets != None):
            return segmentation(first_packets.packet_type, first_packets.source, first_packets.dest,
                                first_packets.session, first_packets.udp_data)
        
        elif (second_packets != None and last_packets != None):
            next_packet = second_packets
            total_seq = last_packet.seq
            cur_seq = next_packet.seq
            packetdata = bytearray()

            while (cur_seq < total_seq and next_packet != None):
                cur_seq = next_packet.seq
                packetdata.extend(next_packet.udp_data)
                next_packet = self.find_next_packet(self, cur_seq, packets)


            if (cur_seq == total_seq):
                return segmentation(second_packets.packet_type, second_packets.source, second_packets.destination,
                                        second_packets.session, bytes(packetdata))
            else:
                raise Exception("not all packets are available!")
        else:
            raise Exception("not all packets are available!")
    def find_packet(self, sequence, packets):
        value = None
        for pack in packets:
            if ((pack.packet_flags == 0x00 or pack.packet_flags == 0x02) and len(pack.udp_data) + sequence == pack.sequence):
                returnValue = pack
                break
        return value

    def disintegrate(self, packet_type, source, dest, session, udp_data):
        packets = []

        udp_data_segments = []
        packet_num = 1

        while (packet_num * payload_lim < len(udp_data)):
            udp_data_segments.append(udp_data[(packet_num - 1) * payload_lim:packet_num * payload_lim])
            packet_num += 1

        udp_data_segments.append(udp_data[(packet_num - 1) * payload_lim:])
        sequence = 0
        for i, udp_data_segment in enumerate(udp_data_segments):
            flags = 0
            if (len(udp_data_segments) == 1):
                flags = 0x03
            elif (len(udp_data_segments) > 1 and i == 0):
                flags = 0x01
            elif (len(udp_data_segments) > 1 and i == (len(udp_data_segments) - 1)):
                flags = 0x02
            else:
                flags = 0x00

            sequence += len(udp_data_segment)
            packets.append(Pack(packet_type, flags, source, dest, session, sequence, udp_data_segment))

        return packets


    def get_packets(self):
        return self.split_packets(self.packet_type, self.source, self.dest, self.session, self.udp_data)
    
    def get_collection(self):
        if (self.packet_type == 0x00):
            return KAM(self.source, self.dest, self.session)
        if (self.packet_type == 0x01):
            return RUM(False, self.source, self.dest, self.session, self.udp_data)
        if (self.packet_type == 0x02):
            return RFRUM(self.source, self.dest, self.session)
        if (self.packet_type == 0x03):
            return RUM(True, self.source, self.dest, self.session, self.udp_data)
        if (self.packet_type == 0x04):
            return SendIdentityMessage(self.source, self.dest, self.session, self.udp_data)
        # if (self.packet_type==0x05):
        #    return GroupMessage(self.source, self.destination, self.session_id, self.data)
        if (self.packet_type == 0x06):
            return SM(self.source, self.dest, self.session, self.udp_data)
        if (self.packet_type == 0x07):
            return BM(self.source, self.dest, self.session, self.udp_data)
    
    












