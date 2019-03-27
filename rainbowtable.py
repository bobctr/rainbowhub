import configparser
import hashlib
import random
import logging
import pickle
import itertools
import constants
from algorithm import Algorithm


class RainbowTable:


    def load_config(self):
        """
        loads configuration from config.ini
        """
        logging.basicConfig(
            filename='log/rainbowTable.log',
            level=logging.DEBUG,
        )
        logging.debug("loading configuration")
        self.config = configparser.ConfigParser()
        self.config.read(constants.MAIN_CONFIG_FILE)
        logging.debug(self.config)


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
        self.load_config()

        # load algorithm TODO manage arguments properly
        if(algorithm == "sha1"):
            self.algorithm = Algorithm.SHA1
        elif(algorithm == "md5"):
            self.algorithm = Algorithm.MD5
        else:
            raise ValueError("Algorithm not supported")

        # load charset
        if(self.config is not None and charset not in self.config[constants.CHARSETS_SECTION]):
            raise ValueError(
                "Charset not supported. For custom charset, edit the file config/config.ini"
            )
        self.charset = self.config[constants.CHARSETS_SECTION][charset]

        self.min_length = min_length
        self.max_length = max_length
        self.chain_length = chain_length
        self.number_of_chains = number_of_chains


    def hash_function(self, plaintext):
        """Returns a string that contains the computed hash of the 
        given string, using the algorithm chosen

        Arguments:
                plaintext {string} -- plaintext to hash

        Returns:
                string -- the hash computed
        """
        if(self.algorithm == Algorithm.SHA1):
            return hashlib.sha1(plaintext.encode('utf-8')).digest()
        elif(self.algorithm == Algorithm.MD5):
            return hashlib.md5(plaintext.encode('utf-8')).digest()


    def reduce_function(self, hashstring, index):
        """Returns a string that contains the reduced value of the 
        given hash string

        Arguments:
                plaintext {string} -- hash to reduce
                index {int} -- affects the choice of the function
                    (for different index, different function)

        Returns:
                string -- the hash computed
        """
        reduced_value = ""
        pswLength = hashstring[1] % (
            self.max_length - self.min_length + 1) + self.min_length
        for i in range(pswLength):
            value = hashstring[((index + i) % len(hashstring))]
            reduced_value += self.charset[value % len(self.charset)]
        return reduced_value


    def generate_chain(self, password):
        '''produces a chain starting from a plaintext
        
        Arguments:
            password {string} -- plaintext to start from
        
        Returns:
            string -- the final hash (chain tail)
        '''
        logging.debug("Starting generating chain...")
        reduced = password
        for i in range(self.chain_length):
            hashed = self.hash_function(reduced)
            logging.debug(reduced + "-->" + hashed.hex())
            reduced = self.reduce_function(hashed, i)
        logging.debug(
            "------------------------------------->" + hashed.hex())
        return hashed


    def generate_table(self):
        '''generates the full table
        '''
        collisions = 0
        self.table = {}
        for _ in range(self.number_of_chains):
            # generates a random password of allowed length
            randomPassword = ''.join(random.choices(
                self.charset,
                k = random.randint(self.min_length, self.max_length))
            )

            chainTail = self.generate_chain(randomPassword)
            if(chainTail in self.table):
                collisions += 1
            self.table[chainTail] = randomPassword
        logging.debug("collisions detected: " + str(collisions))


    def save_to_file(self, filename):
        '''writes this object on a file
        
        Arguments:
            filename {string} -- output file path
        
        Returns:
            bool -- true if success
        '''
        if (filename is None):
            return False
        fd = open(filename, "wb")
        if(fd.write(pickle.dumps(self)) > 0):
            return True
        return False


    @staticmethod
    def load_from_file(filename):
        '''loads a RainbowObject previously generated
        
        Arguments:
            filename {string} -- input file path
        
        Raises:
            ValueError -- if the file does not contain a valid object
        
        Returns:
            RainbowTable -- the loaded object
        '''
        with open(filename, 'rb') as inputFile:
            objectLoaded = pickle.load(inputFile)
        if(not isinstance(objectLoaded, RainbowTable)):
            raise ValueError("The file " + filename +
                             " does not contain a valid table")
        return objectLoaded


    def lookup(self, hash_to_crack):
        '''looks for a cracked hash
        
        Arguments:
            hash_to_crack {string}
        
        Returns:
            the plaintext if found, None otherwise
        '''
        if(hash_to_crack in self.table):
            logging.debug("first chain matched: " +
                  self.table[hash_to_crack] + " --> " + hash_to_crack)
            return self.crack(self.table[hash_to_crack], hash_to_crack)
        for i in range(self.chain_length-1, -1, -1):
            hashtemp = hash_to_crack
            for j in range(i, self.chain_length):
                reduced = self.reduce_function(hashtemp, j)
                hashtemp = self.hash_function(reduced)
                if(hashtemp in self.table):
                    logging.debug(
						"chain matched: " + 
						self.table[hashtemp] + 
						" --> " + 
						hashtemp.hex() + 
						" after " + 
						str(self.chain_length-i) + 
						" iterations"
                    )
                    psw = self.crack(self.table[hashtemp], hash_to_crack)
                    if(psw is not None):
                        return psw
        return None


    def crack(self, chainhead, hash_to_crack):
        '''tries to crack a given hash on a single chain
        
        Arguments:
            chainhead {string} -- chain head
            hash_to_crack {string}
        
        Returns:
            string -- the plaintext if found, None otherwise
         '''
        reduced = chainhead
        for i in range(self.chain_length):
            hashtemp = self.hash_function(reduced)
            if(hashtemp == hash_to_crack):
                return reduced
            reduced = self.reduce_function(hashtemp, i)
        return None

