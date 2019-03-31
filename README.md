# RainbowHub
[![CircleCI](https://circleci.com/gh/bobctr/rainbowhub.svg?style=svg)](https://circleci.com/gh/bobctr/rainbowhub) [![codecov](https://codecov.io/gh/bobctr/rainbowhub/branch/master/graph/badge.svg)](https://codecov.io/gh/bobctr/rainbowhub)


Simple Rainbow tables implementation.

## What is a rainbow table?
https://en.wikipedia.org/wiki/Rainbow_table

https://www.geeksforgeeks.org/understanding-rainbow-table-attack/

## What I have learned
The purpose of this project is to understand how a rainbow table is implemented and used, with a practical approach.
While developing, I found myself dealing with various challenges, that gave me a deeper understanding on:

  1. **How hashing and rainbow tables work**, and how some hashing algorithms can be exploited efficiently, finding the compromise between a brute-force approach and a pure lookup table
  2. How to master and combine common **data structures** to build an efficient solution (lists, dictionaries, ...)
  3. Python API and modules such as
     * _argparse_ -- to easily handle arguments for my scripts
     * _hashing_ -- to use SHA1 and MD5 hash functions
     * _pickle_ -- to store in a file the generated table, and restore it for cracking
     * _itertools_ -- to generate random passwords to start chains with
  4. Python **Unit Tests** run with _pytest_ module
  5. Continuous Integration (build, test, code coverage on **CircleCI**) 

## Key features
  - Custom rainbow table generator
  - SHA1 and MD5 support
  - Table serialization
  
------

### Configuration
All the charset available with their respective names are written in ```config/config.ini```.
If you want to add a custom one, just add it at the end of the file.

### Run
To generate a new table:

```
python3 rainbowgen.py algorithm_name charset_name min_password_length max_massword_length chain_length n_chains output_file
```

To try cracking a hash:

```
python3 rainbowcrack.py hash_string table_file
```

Example:
```
python3 rainbowgen.py sha1 alphanumeric 1 6 20 1000 new_table.rt
python3 rainbowcrack.py "1e4e888ac66f8dd41e00c5a7ac36a32a9950d271" new_table.rt
```
