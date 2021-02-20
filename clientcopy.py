#import wmi
import csv
import socket
import hashlib
import re, uuid

#c = wmi.WMI()

TCP_IP = 'blockvote.ddns.net'
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
#def createNodeID():
    #MACAddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    #HardDriveSerialNumber = c.Win32_PhysicalMedia()[0].wmi_property('SerialNumber').value.strip()
    #NodeID = SHA256ENC(MACAddress + HardDriveSerialNumber)
    #return NodeID


# Takes the .csv named knownNodes.csv and turns it into an array
def createNodeIDList():
    nodeListFilename = 'knownNodes.csv'
        
    Nodes = []
        
    with open(nodeListFilename, 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            Nodes.append(row)
            print(row)
            
    return Nodes
    
    
# Searches through the array of nodes and checks if your NodeID is in that List
def searchNodeIDList(NodeID, NodeIDList):
    if NodeID in NodeIDList:
        return True
    else:
        return False
    

def updateNodeIDList(Nodes):
    nodeListFilename = 'knownNodes.csv'
        
    with open(nodeListFilename, 'w') as fd:
        writer = csv.writer(fd)
        for node in Nodes:
            writer.writerow([node])
    
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
            
    '''
    with open('received_file', 'wb') as f:
        print ('file opened')
        while True:
            #print('receiving data...')
            data = s.recv(BUFFER_SIZE)
            print('data=%s', (data))
            if not data:
                f.close()
                print ('file close()')
                break
            # write data to a file
            f.write(data)

    print('Successfully get the file')
    '''
    
    clientSocket.close()
    print('connection closed')

if __name__ == "__main__":
    #NodeID = createNodeID()
    #NodeList = createNodeIDList()
    #nodeIDinList = searchNodeIDList(NodeID, NodeList)
    #print(nodeIDinList)
    
    # If the ID isn't in the list append the ID to the list
    #if nodeIDinList == False:
    #    NodeList.append(NodeID)
        
    # Overwrite contents of .csv file with updated data
    #updateNodeIDList(NodeList)
    while True:
        main()
