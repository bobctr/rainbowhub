import argparse
import sys
from RainbowTable import RainbowTable

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", help="sha1 or mda5")
    parser.add_argument("charset", help="charset must be included in config.ini")
    parser.add_argument("min_length", help="minimum length of passwords",type=int)
    parser.add_argument("max_length", help="maximum length of passwords",type=int)
    parser.add_argument("max_length", help="maximum length of passwords",type=int)
    parser.add_argument("chain_length", help="length of each chain",type=int)
    parser.add_argument("number_of_chains", help="number of chains generated",type=int)
    args = parser.parse_args()

    rt = RainbowTable(args.algorithm, args.charset, args.min_length, args.max_length, args.chain_length, args.number_of_chains)

    #TODO log
    print(rt.algorithm)
    print(rt.charset)
    print(rt.min_length)
    print(rt.max_length)
except:
    e = sys.exc_info()[0]
    print(e)