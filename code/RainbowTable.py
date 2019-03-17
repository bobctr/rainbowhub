import code.constants as constants
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
        self.config = configparser.ConfigParser()
        self.config.read(constants.MAIN_CONFIG_FILE)

    def __init__(self, algorithm, charset, min_length, max_length, 
                chain_length, number_of_chains):
        """RainbowTable constructor
        
        Arguments:
            algorithm {string} -- name of hash algorithm used
            charset {string} -- name of charset
            min_length {int} -- minimum passwords length
            max_length {int} -- maximum password length
            chain_length {int} -- chain length
            number_of_chains {int} -- number of chains
        
        Raises:
            ValueError -- if algorithm is not 'sha1' or 'md5'
            ValueError -- if charset name is not in config file
        """
        self.updateConfig()

        # load algorithm TODO manage arguments properly
        if(algorithm == "sha1"):
            self.algorithm = Algorithm.SHA1
        elif(algorithm == "md5"):
            self.algorithm = Algorithm.MD5
        else:
            raise ValueError("Algorithm not supported")
              
        # load charset
        if(self.config[constants.CHARSETS_SECTION][charset] is None):
            raise ValueError("Charset not supported. For custom charset, edit the file config.ini")
        self.charset = self.config[constants.CHARSETS_SECTION][charset]

        self.min_length = min_length
        self.max_length = max_length
        self.chain_length = chain_length
        self.number_of_chains = number_of_chains
    
    def hashFunction(self, plaintext):
        """Returns a string that contains the computed hash of the 
        given string, using the algorithm chosen
        
        Arguments:
            value {string} -- plaintext to hash
        
        Returns:
            string -- the hash computed
        """
        if(self.algorithm == Algorithm.SHA1):
            return hashlib.sha1(plaintext.encode('utf-8')).hexdigest()
        elif(self.algorithm == Algorithm.MD5):
            return hashlib.md5(plaintext.encode('utf-8')).hexdigest()

    def reduceFunction(self, hashString, index):
        reducedValue = ""
        randomInt = random.randint(self.min_length, self.max_length)
        for i in range(randomInt):
            value = hashString[((index + i) % len(hashString))]
            reducedValue += self.charset[(ord(value) ^ 31) % len(self.charset)]                       
        return reducedValue
    
    def generateChain(self, password):
        reduced = password
        for i in range(self.chain_length):
            hashTemp = self.hashFunction(reduced)
            reduced = self.reduceFunction(hashTemp,i)
            logging.debug('generated tuple: (%s,%s)', hashTemp, reduced)
        logging.debug('final generated tuple: (%s,%s)', password, hashTemp)
        return hashTemp

    def generateTable(self):
        collisions = 0
        self.table = {}
        for _ in range(self.number_of_chains):
            randomPassword = ''.join(random.sample(self.charset, random.randint(self.min_length, self.max_length)))
            chainTail = self.generateChain(randomPassword)
            if(chainTail in self.table):
                collisions += 1
            else:
                self.table[chainTail] = randomPassword
        logging.debug("collisions detected: " + str(collisions))

    def saveToFile(self, fileName):
        if (fileName is None):
            return False
        fd = open(fileName, "wb")
        if(fd.write(pickle.dumps(self)) > 0):
            return True
        return False
 
    @staticmethod
    def loadFromFile(fileName):
        try:
            fd = open(fileName, "rb")
        except IOError:
            logging.error("File " + fileName + " not found")
        
        objectLoaded = pickle.load(fd)
        if(type(objectLoaded) is RainbowTable):
            return objectLoaded
        return None

    def lookup(self, hashToCrack):
        if(hashToCrack in self.table):
            return self.crack(self.table[hashToCrack], hashToCrack)
        for i in range(self.chain_length-1, -1, -1):
            hashTemp = hashToCrack
            for j in range(i, self.chain_length):
                reduced = self.reduceFunction(hashTemp, j)
                hashTemp = self.hashFunction(reduced)
                if(hashTemp in self.table):
                    return self.crack(self.table[hashTemp], hashToCrack)
        return None
      
    def crack(self, chainHead, hashToCrack):
        reduced = chainHead
        for i in range(self.chain_length):
            hashTemp = self.hashFunction(reduced)
            if(hashTemp == hashToCrack):
                return reduced
            reduced = self.reduceFunction(hashTemp, i)
        return None