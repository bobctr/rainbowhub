import constants
from algorithms import Algorithms
import configparser
import hashlib
import random
import logging
import string


class RainbowTable:

    def updateConfig(self):
        """load configuration from config.ini and set logger
        """
        logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
        self.config = configparser.ConfigParser()
        self.config.read(constants.MAIN_CONFIG_FILE)
        #TODO log


    def __init__(self, algorithm, charset, min_length, max_length, chain_length, number_of_chains):
        self.updateConfig()
        
        #load algorithm
        if(algorithm == "sha1"):
            self.algorithm = Algorithms.SHA1
        elif(algorithm == "mda5"):
            self.algorithm = Algorithms.MD5
        else:
            raise ValueError("Algorithm not supported")
              
        #load charset
        if(self.config[constants.CHARSETS_SECTION][charset] == None):
            raise ValueError("Charset not supported. For custom charset, edit the file config.ini")
        self.charset = self.config[constants.CHARSETS_SECTION][charset]

        self.min_length = min_length
        self.max_length = max_length
        self.chain_length = chain_length
        self.number_of_chains = number_of_chains
    

    def hashFunction(self, value):
        if(self.algorithm == Algorithms.SHA1):
            return hashlib.sha1(value.encode('utf-8')).hexdigest()
        elif(self.algorithm == Algorithms.MD5):
            return hashlib.md5(value)

    
    def reduceFunctionSHA1(self, hashString, index):
        reducedValue = ""
        for i in range(random.randint(self.min_length,self.max_length)):
            reducedValue = reducedValue + hashString[((index + i) ^ 31) % 15]
        return reducedValue


    def reduceFunctionMD5(self, hashString, index):
        pass


    def reduceFunction(self, hashString, index):
        if(self.algorithm == Algorithms.SHA1):
            return self.reduceFunctionSHA1(hashString, index)
        elif(self.algorithm == Algorithms.MD5):
            return self.reduceFunctionMD5(hashString, index)

    
    def generateChain(self, password):
        reduced = password
        for i in range(self.chain_length):
            hash = self.hashFunction(reduced)
            reduced = self.reduceFunction(hash,i)
            print('generated tuple: (%s,%s)',hash,reduced)
        logging.debug('final generated tuple: (%s,%s)',password,hash)
        return (password, hash)


    def generate(self):
        collisions = 0
        self.table = {}
        for i in range(self.number_of_chains):
            randomPassword = ''.join(random.sample(self.charset,random.randint(self.min_length,self.max_length)))
            newChain = self.generateChain(randomPassword)
            if(newChain in self.table):
                collisions += 1
            else:
                self.table[i] = newChain
        print("collisions: " + str(collisions))
        print(self.table)


    def serialize(self, parameter_list):
        pass


if __name__ == "__main__":
    test = RainbowTable("sha1","alphanumeric",5,10,20,30)
    test.generate()