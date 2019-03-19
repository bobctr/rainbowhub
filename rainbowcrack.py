import sys
import os
import argparse
from RainbowTable import RainbowTable 

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("hash_string", help="hash to crack")
    parser.add_argument("rainbow_table_file", help="name of file containing a valid rainbow table"
    "(generated from rainbowgen.py)")
    args = parser.parse_args()

    rt = RainbowTable.loadFromFile(args.rainbow_table_file)
    psw = rt.lookup(args.hash_string)
    if(psw is not None):
        print("Candidate found: " + psw)
    print("No match found")

except Exception as e:
    print("ERROR: " + e)