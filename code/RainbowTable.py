import code.constants
from code.algorithm import Algorithm
import configparser
import hashlib
import random
import logging
import pickle
import itertools


class RainbowTable:

    def updateConfig(self):
        """
        loads configuration from config.ini and sets logger
        """
        #logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        self.config = configparser.ConfigParser()
        self.config.read(code.constants.MAIN_CONFIG_FILE)
        #TODO log


    def __init__(self, algorithm, charset, min_length, max_length, chain_length, number_of_chains):
        self.updateConfig()
        
        #load algorithm TODO manage arguments better
        if(algorithm == "sha1"):
            self.algorithm = Algorithm.SHA1
        elif(algorithm == "md5"):
            self.algorithm = Algorithm.MD5
        else:
            raise ValueError("Algorithm not supported")
              
        #load charset
        if(self.config[code.constants.CHARSETS_SECTION][charset] == None):
            raise ValueError("Charset not supported. For custom charset, edit the file config.ini")
        self.charset = self.config[code.constants.CHARSETS_SECTION][charset]

        self.min_length = min_length
        self.max_length = max_length
        self.chain_length = chain_length
        self.number_of_chains = number_of_chains
    

    def hashFunction(self, value):
        if(self.algorithm == Algorithm.SHA1):
            return hashlib.sha1(value.encode('utf-8')).hexdigest()
        elif(self.algorithm == Algorithm.MD5):
            return hashlib.md5(value.encode('utf-8')).hexdigest()

    
    def reduceFunctionSHA1(self, hashString, index):
        reducedValue = ""
        randomInt = random.randint(self.min_length,self.max_length)
        for i in range(randomInt):
            reducedValue += hashString[((index + i) ^ 31) % len(hashString)]
        return reducedValue


    def reduceFunctionMD5(self, hashString, index):
        raise NotImplementedError()


    def reduceFunction(self, hashString, index):
        if(self.algorithm == Algorithm.SHA1):
            return self.reduceFunctionSHA1(hashString, index)
        elif(self.algorithm == Algorithm.MD5):
            return self.reduceFunctionMD5(hashString, index)

    
    def generateChain(self, password):
        reduced = password
        for i in range(self.chain_length):
            hashTemp = self.hashFunction(reduced)
            reduced = self.reduceFunction(hashTemp,i)
            logging.debug('generated tuple: (%s,%s)',hashTemp,reduced)
        logging.debug('final generated tuple: (%s,%s)',password,hashTemp)
        return hashTemp


    def generateTable(self):
        collisions = 0
        self.table = {}
        for _ in range(self.number_of_chains):
            randomPassword = ''.join(random.sample(self.charset,random.randint(self.min_length,self.max_length)))
            chainTail = self.generateChain(randomPassword)
            if(chainTail in self.table):
                collisions += 1
            else:
                self.table[chainTail] = randomPassword
        logging.debug("collisions detected: " + str(collisions))


    def saveToFile(self, fileName):
        if (fileName is None):
            return False
        fd = open(fileName,"wb")
        if(fd.write(pickle.dumps(self)) > 0):
            return True
        return False

    
    @staticmethod
    def loadFromFile(fileName):
        try:
            fd = open(fileName,"rb")
        except IOError:
            logging.error("File " + fileName + " not found")
        
        objectLoaded = pickle.load(fd)
        if(type(objectLoaded) is RainbowTable):
            return objectLoaded
        return None


    def lookup(self, hashToCrack):
        if(hashToCrack in self.table):
            return self.crack(self.table[hashToCrack],hashToCrack)
        for i in range(self.chain_length-1, -1 , -1):
            hashTemp = hashToCrack
            for j in range(i,self.chain_length):
                reduced = self.reduceFunction(hashTemp,j)
                hashTemp = self.hashFunction(reduced)
                if(hashTemp in self.table):
                    return self.crack(self.table[hashTemp],hashToCrack)
        return None

        
    def crack(self, chainHead, hashToCrack):
        reduced = chainHead
        for i in range(self.chain_length):
            hashTemp = self.hashFunction(reduced)
            if(hashTemp == hashToCrack):
                return reduced
            reduced = self.reduceFunction(hashTemp,i)
        return None 
                    




if __name__ == "__main__":
    test = RainbowTable("sha1","alphanumeric",2,2,20,20)
    test.generateTable()
    print(test.table)
    found = 0
    for perm in itertools.permutations("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",2):
        passw = test.lookup(test.hashFunction(''.join(perm)))
        if(passw is not None):
            print(passw)
            found += 1
    print('found ' + str(found))
        
    print("cia")