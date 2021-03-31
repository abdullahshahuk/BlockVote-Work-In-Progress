import csv
import socket
import hashlib
import platform
import re, uuid
import wmi

TCP_IP = 'blockvote2.ddns.net'
TCP_PORT = 5006
BUFFER_SIZE = 1024

# Encodes a string with SHA256 Encoding
def SHA256ENC(string):
    hash_func = hashlib.sha256()
    encoded_string=string.encode()
    hash_func.update(encoded_string)
    message = hash_func.hexdigest()
    return message

# Generates NodeID from the Hash of the MAC Address + the Hard Drive serial number.
def createNodeID():
    c = wmi.WMI()
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


def main():
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((TCP_IP, TCP_PORT))
    
    pendingTransmissionFile = 'pendingTransmission.txt'
    pendingTransmission = open(pendingTransmissionFile,'rb')
    while True:
        l = pendingTransmission.read(BUFFER_SIZE)
        while (l):
            clientSocket.send(l)
            l = pendingTransmission.read(BUFFER_SIZE)
        if not l:
            pendingTransmission.close()
            clientSocket.close()
            break
    
    clientSocket.close()
    print('connection closed')

    #Clears pending transmission after file has been sent.
    open(pendingTransmissionFile, 'w').close()

if __name__ == "__main__":

    # Determine NodeID
    NodeID = createNodeID()

    # Reads knownNodes.csv and converts it into a variable
    NodeList = createNodeIDList()

    # Searches Nodes to see if NodeID is found
    nodeIDinList = searchNodeIDList(NodeID, NodeList)

    # If the ID isn't in the list append the ID to the list
    if nodeIDinList == False:
        NodeList.append(NodeID)
        
    # Overwrite contents of knownNodes.csv file with updated data
    updateNodeIDList(NodeList)

    # Currently an endless loop
    while True:
        main()
