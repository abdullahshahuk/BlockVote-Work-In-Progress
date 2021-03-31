# Handling MAC Addresses

import re, uuid
MACAddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
print ('\nMAC Address: ' + MACAddress + '\n')

# Windows specific hard drive serial number code (Needs linux version)
import wmi

c = wmi.WMI()
HardDriveSerialNumber = c.Win32_PhysicalMedia()[0].wmi_property('SerialNumber').value.strip()
print('Hard Drive Serial Number: ' + HardDriveSerialNumber + '\n')

# Creating NodeID from SHA256 hash of the MAC address and the hard drive serial number to make a unique identifier to match the IP
# This is important as it allows a new IP to be assigned to a machine when its dynamic IP changes
# This should help reduce the required filesize of the database that holds node information reducing 'bloat'

import hashlib

def SHA256ENC(string):
    hash_func = hashlib.sha256()
    encoded_string=string.encode()
    hash_func.update(encoded_string)
    message = hash_func.hexdigest()
    return message

NodeID = SHA256ENC(MACAddress + HardDriveSerialNumber)

print('Node ID: ' + NodeID + '\n')

# Handling the data storage (Storing the Node ID's and associating them with the IP addresses of each device) 

import csv
import numpy

def createNodeID():
    MACAddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    HardDriveSerialNumber = c.Win32_PhysicalMedia()[0].wmi_property('SerialNumber').value.strip()
    NodeID = SHA256ENC(MACAddress + HardDriveSerialNumber)
    return NodeID

# Takes the .csv named knownNodes.csv and turns it into an array
def createNodeIDList():
    nodeListFilename = 'knownNodes.csv'
        
    Nodes = []
        
    with open(nodeListFilename, 'r', newline='') as fd:
        reader = csv.reader(fd)
        for row in reader:
            Nodes.append(row)
            #print(row)
            #print(Nodes)
            
    return Nodes

# Searches through the array of nodes and checks if your NodeID is in that List
def searchNodeIDList(NodeID, NodeIDList):
    print(NodeIDList)
    NodeID = NodeID.split(",")
    print(NodeID)
    if NodeID in NodeIDList:
        return True
    else:
        return False
    

def updateNodeIDList(Nodes):
    nodeListFilename = 'knownNodes.csv'

    #print(Nodes)
        
    with open(nodeListFilename, 'w', newline='') as fd:
        writer = csv.writer(fd)
        for node in Nodes:
            writer.writerow([str(node).translate({ord('['): '', ord(']'): '', ord('\''): ''})])
            #print(node)


NodeID = createNodeID()
NodeList = createNodeIDList()
nodeIDinList = searchNodeIDList(NodeID, NodeList)
print(nodeIDinList)
    
# If the ID isn't in the list append the ID to the list
if nodeIDinList == False:
    NodeList.append(NodeID)
        
# Overwrite contents of .csv file with updated data
updateNodeIDList(NodeList)