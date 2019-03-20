#import code.constants as constants
#from code.algorithm import Algorithm
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
	
	def hashFunction(self, plaintext):
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

	def reduceFunction(self, hashString, index):
		reducedValue = ""
		pswLength = hashString[1] % (self.max_length - self.min_length + 1) + self.min_length
		#ran+ "-->" +domInt = random.randint(self.min_length, self.max_length)
		for i in range(pswLength):
			value = hashString[((index + i) % len(hashString))]
			reducedValue += self.charset[value % len(self.charset)]                       
		return reducedValue
	
	def generateChain(self, password):
		reduced = password
		for i in range(self.chain_length):
			hashTemp = self.hashFunction(reduced)
			logging.debug(reduced + "-->" + hashTemp.hex())
			reduced = self.reduceFunction(hashTemp,i)
		logging.debug("------------------------------------->" + hashTemp.hex())
		return hashTemp

	def generateTable(self):
		collisions = 0
		self.table = {}
		for _ in range(self.number_of_chains):
			#generates a random password of allowed length
			randomPassword = ''.join(random.choices(
				self.charset, 
				k=random.randint(self.min_length, self.max_length))
			)
			chainTail = self.generateChain(randomPassword)
			if(chainTail in self.table):
				collisions += 1
				#print("collision")
				logging.debug("collides")
			self.table[chainTail] = randomPassword
			#print (self.table[chainTail] + " --> " + randomPassword)
		print("collisions: " + str(collisions))

	def saveToFile(self, fileName):
		if (fileName is None):
			return False
		fd = open(fileName, "wb")
		if(fd.write(pickle.dumps(self)) > 0):
			return True
		return False
 
	@staticmethod
	def loadFromFile(fileName):
		with open(fileName, 'rb') as inputFile:				
			objectLoaded = pickle.load(inputFile)
		if(not isinstance(objectLoaded, RainbowTable)):
			raise ValueError("The file " + fileName + " does not contain a valid table")
		return objectLoaded
		
	def lookup(self, hashToCrack):
		if(hashToCrack in self.table):
			print("first chain matched: " + self.table[hashToCrack] + " --> " + hashToCrack)
			return self.crack(self.table[hashToCrack], hashToCrack)
		for i in range(self.chain_length-1, -1, -1):
			hashTemp = hashToCrack
			for j in range(i, self.chain_length):
				reduced = self.reduceFunction(hashTemp, j)
				hashTemp = self.hashFunction(reduced)
				if(hashTemp in self.table):
					print("chain matched: " + self.table[hashTemp] + " --> " 
						+ hashTemp.hex() + " after " + str(self.chain_length-i) + " iterations"
					)
					psw = self.crack(self.table[hashTemp], hashToCrack)
					if(psw is not None):
						return psw
		return None
	  
	def crack(self, chainHead, hashToCrack):
		reduced = chainHead
		for i in range(self.chain_length):
			hashTemp = self.hashFunction(reduced)
			if(hashTemp == hashToCrack):
				return reduced
			reduced = self.reduceFunction(hashTemp, i)
		return None

if __name__ == "__main__":
	rt = RainbowTable.loadFromFile("debugTable.rt")
	psw = rt.lookup("57a1e424f5ae8a1bf2a9a65bffaea7da2a97ec6e")
	print(psw)