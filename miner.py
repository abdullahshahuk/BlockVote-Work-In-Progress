import os
import random
import lib

blockchainz = lib.Blockchain()

# Vars
userList = ["Alice", "Bob", "Anon", "David", "Anon", "Franklin", "Anon", "Harry", "Iris", 
                "Anon", "Kate", "Leo", "Monica", "Anon", "Oscar", "Phoebe", "Quinn", "Anon", 
                "Sofia", "Anon", "Umar", "Victor", "Anon", "Xena", "Anon", "Zara"]

memoList = ["Y", "N", "I"]

receiverList = ["Policy 01", "Policy 02", "Policy 03"]

# Blockchain file handler
filename = 'blockchain.txt'

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
        
blockchainz.difficultyLevel = 1

currentBlock = 0

blockfile = open(filename,append_write)

# Main Loop
while True:
    if (currentBlock < len(blockchainz.chain) - 1):
        print(blockchainz.chain[ len(blockchainz.chain) - 1])
        blockfile.write(str(blockchainz.chain[ len(blockchainz.chain) - 1]))
        currentBlock = currentBlock + 1
    addNBlocks(1)

blockfile.close()