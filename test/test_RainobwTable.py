import os
import sys
import pytest
from RainbowTable import RainbowTable
from algorithm import Algorithm
import string
import hashlib
import uuid
import random

def test_init():
	testTable = RainbowTable("sha1","alphanumeric",1,1,1,1)
	assert testTable.config is not None
	assert testTable.algorithm == Algorithm.SHA1
	assert testTable.charset == "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	with pytest.raises(ValueError):
		testTable = RainbowTable("sha1000","alphanumeric",1,1,1,1)
	with pytest.raises(ValueError):
		testTable = RainbowTable("sha1","charsetnotfound",1,1,1,1)

def test_hashFunction():
	testTable = RainbowTable("sha1","alphanumeric",1,1,1,1)
	assert testTable.hashFunction("rainbowtable") == "ec44b366a89bb2ba78d6b8e5e81194d596d301b7"
	testTable = RainbowTable("md5","alphanumeric",1,1,1,1)
	assert testTable.hashFunction("rainbowtable") == "c055588e18df56f877f3c3ca73790ecd"

def test_reduceFunction():
	testTable = RainbowTable("sha1","alphanumeric",4,7,1,1)
	for i in range(50):
		randomstring = ''.join(random.choices(string.ascii_lowercase, k=5))
		hashString = testTable.hashFunction(randomstring)
		reduced = testTable.reduceFunction(hashString,i)
		assert set(reduced) <= set(testTable.charset)
		assert len(reduced) in range(4,8)

def test_generateTable():
	testTable = RainbowTable("sha1","alphanumeric",2,4,5,30)
	testTable.generateTable()
	for k in testTable.table.keys():
		assert len(k) == 40
		assert len(testTable.table[k]) in range(2,5)

def test_saveAndload(tmpdir):
	testTable = RainbowTable("sha1","alphanumeric",2,4,5,10)
	testTable.generateTable()
	testTable.saveToFile(tmpdir + "/newSerializedTable.rt")
	sameTable = RainbowTable.loadFromFile(tmpdir + "/newSerializedTable.rt")
	assert testTable.table == sameTable.table

