import lib
from lib import Block

class Blockchain:
    
    def __init__(self):
        self.difficultyLevel = 1
        self.chain = [Block.genesis()]
        
    def addBlock(self, record):
        newBlock = Block.mineBlock( self.chain[ len(self.chain) - 1], record, self.difficultyLevel)
        self.chain.append(newBlock)
        
    #def __str__(self):
    #    return self.chain