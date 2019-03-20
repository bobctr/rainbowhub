# RainbowHub
![CircleCI (all branches)](https://img.shields.io/circleci/project/github/bobctr/RainbowHub.svg)

Simple Rainbow tables implementation.

## Key features
  - Custom rainbow table generator
  - SHA1 and MD5 support
  - Table serialization
  
### Configuration
All the charset available with their respective names are written in ```config/config.ini```.
If you want to add a custom one, just add it at the end of the file.


### Run
To generate a new table:

```
python3 rainbowgen.py algorithm_name charset_name min_password_length max_massword_length chain_length n_chains output_file
```

To launch it against a hash:

```
python3 rainbowcrack.py hash_string table_file
```

Example:
```
python3 rainbowgen.py sha1 alphanumeric 1 6 20 1000 new_table.rt
python3 rainbowcrack.py "1e4e888ac66f8dd41e00c5a7ac36a32a9950d271" new_table.rt
```
