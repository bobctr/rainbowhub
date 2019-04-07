# RainbowHub
[![CircleCI](https://circleci.com/gh/bobctr/rainbowhub.svg?style=svg)](https://circleci.com/gh/bobctr/rainbowhub) [![codecov](https://codecov.io/gh/bobctr/rainbowhub/branch/master/graph/badge.svg)](https://codecov.io/gh/bobctr/rainbowhub)


Simple Rainbow tables implementation.

## What a rainbow table is and how it is implemented
https://en.wikipedia.org/wiki/Rainbow_table

https://www.geeksforgeeks.org/understanding-rainbow-table-attack/

A **rainbow table** is a complex data structure used for hash cracking, whose main goal is making the task significantly more time-efficient than brute-forcing, while keeping the space on disk needed very small compared to hash tables.

Rainbow tables contains *precomputed hash chains*, which are generated with a sequence of hash/reduce function application on a starting random plaintext, where only the head and the tail of each chain are stored
These chains are then used during the cracking process, when the target hash is reduced/hashed multiple times until a match with a chain tail is found.
After that, the corresponding chain is generated again until the target hash is matched.

Rainbow tables can be easily countered adding a *salt* (small random string of bytes) to a stored hash.

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
To generate a new table

```
python3 rainbowgen.py algorithm_name charset_name min_password_length max_massword_length chain_length n_chains output_file
```
- ```algorithm_name```: name of the hashing algorithm (currently SHA1 and MD5 are available)
- ```charset_name```: name of the charset used to generate random plaintext (available charsets are defined in settings.py)
- ```min_password_length```
  ```max_password_length```: range for random plaintext length
- ```chain_length```: number of *hash/reduce* iterations for each chain
- ```n_chains```: number of tuples *head_plaintext/tail_hash* that will be generated
- ```output_file```: path of output file (conventionally with extension *.rt*)

To try cracking a hash:

```
python3 rainbowcrack.py hash_string table_file
```
- ```hash_string```: string containing the hash to crack
- ```table_file```: file containing the generated rainbow table (conventionally with extension *.rt*)

Example:
```
python3 rainbowgen.py sha1 alphanumeric 1 6 20 1000 test_table.rt
python3 rainbowcrack.py "1e4e888ac66f8dd41e00c5a7ac36a32a9950d271" test_table.rt
```
