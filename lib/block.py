import datetime
import hashlib

def SHA256ENC(string):
    hash_func = hashlib.sha256()
    encoded_string=string.encode()
    hash_func.update(encoded_string)
    message = hash_func.hexdigest()
    return message


class Block:
    
    def __init__(self, index, timestamp, previousHash, record, difficultyLevel):
        self.index = index
        self.timestamp = timestamp
        self.record = record
        self.previousHash = previousHash
        proofOfWork = self.proofOfWork(difficultyLevel)
        self.hash = proofOfWork[0]
        self.nonce = proofOfWork[1]
        
    def __str__(self):
        blockreturn = ("\nIndex: " + str(self.index) + 
                       "\nTimestamp: " + str(self.timestamp) + 
                       "\nRecord: " + str(self.record) +
                       "\nPrevious Hash : " + str(self.previousHash) +
                       "\nHash : " + str(self.hash) +
                       "\nNonce : " + str(self.nonce))
         
        return blockreturn
        
    def genesis():
        blocka = Block(
            0,
            datetime.datetime.now(),
            "",
            "GENESIS",
            1
            )
        
        return blocka
        
        
    def mineBlock(previousBlock, record, difficultyLevel):
        index = previousBlock.index + 1
        timestamp = str(datetime.datetime.now())
        previousHash = previousBlock.hash
        return Block(index, timestamp, previousHash, record, difficultyLevel)
    
    
    def computeHash(self, msg):
        return SHA256ENC(str(msg))
    
    
    def proofOfWork(self, difficultyLevel):
        
        message = str(self.timestamp) + str(self.record) + str(self.previousHash)
        
        if difficultyLevel:
            leadingZeros = "3"*difficultyLevel
            nonce = 0
            
            while True:
                hash = Block.computeHash(self, message + str(nonce))
                if hash[0 : difficultyLevel] == leadingZeros:
                    return hash, nonce
                nonce = nonce + 1
                
        else:
            hash = Block.computeHash(message)
            nonce = 0
            return hash, nonce