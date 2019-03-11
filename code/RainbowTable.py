import constants
from algorithms import Algorithms
import configparser


class RainbowTable:
    def update_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(constants.MAIN_CONFIG_FILE)
        #TODO log

    def __init__(self, algorithm, charset, min_length, max_length, chain_length, number_of_chains):
        self.update_config()
        if(algorithm == "sha1"):
            self.algorithm = Algorithms.SHA1
        elif(algorithm == "mda5"):
            self.algorithm = Algorithms.MDA5        
        if(not self.config[constants.CHARSETS_SECTION][charset] == None):
            self.charset = charset

        self.min_length = min_length
        self.max_length = max_length
        self.chain_length = chain_length
        self.number_of_chains = number_of_chains

    