import os
import random
import lib
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

#######
#######
#######

blockchainz = lib.Blockchain()

# Vars
userList = ["Alice", "Bob", "Anon", "David", "Anon", "Franklin", "Anon", "Harry", "Iris", 
                "Anon", "Kate", "Leo", "Monica", "Anon", "Oscar", "Phoebe", "Quinn", "Anon", 
                "Sofia", "Anon", "Umar", "Victor", "Anon", "Xena", "Anon", "Zara"]

memoList = ["Y", "N", "I"]

receiverList = ["Policy 01", "Policy 02", "Policy 03"]

# Blockchain file handler
filename = 'pendingTransmission.txt'

if os.path.exists(filename):
    append_write = 'a' # append if already exists
else:
    append_write = 'w' # make a new file if not

# Appends Blocks
def addNBlocks(n):
    for i in range(n):
        sender = userList[random.randint(0, len(userList) - 1)],
        receiver = receiverList[random.randint(0, len(receiverList) - 1)],
        memo = memoList[random.randint(0, len(memoList) - 1)],
        amount = 1
        blockchainz.addBlock(
            record = [sender, receiver, memo, amount]
        )
        
blockchainz.difficultyLevel = 5

currentBlock = 0

###########
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
############

# Main Loop
while True:
    blockfile = open(filename,append_write)
    print("Opened blockchain file")
    if (currentBlock < len(blockchainz.chain) - 1):
        print(blockchainz.chain[ len(blockchainz.chain) - 1])
        blockfile.write(str(blockchainz.chain[ len(blockchainz.chain) - 1]))
        currentBlock = currentBlock + 1
    addNBlocks(1)
    print("Created block")
    main()
    print("Sent Block")
    blockfile.close()