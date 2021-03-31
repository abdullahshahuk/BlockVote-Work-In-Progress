import csv

nodeListFilename = 'knownNodes.csv'
        
Nodes = []
        
with open(nodeListFilename, 'r', newline='') as fd:
    reader = csv.reader(fd)
    for row in reader:
        Nodes.append(row)
        print(row)

print('\nEntire Array\n')
print(Nodes)
print('\nFinished Reading\n')
        
with open(nodeListFilename, 'w', newline='') as fd:
    writer = csv.writer(fd)
    for node in Nodes:
        writer.writerow(node)
        print(node)