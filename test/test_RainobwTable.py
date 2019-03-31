import pytest
import string
import hashlib
import uuid
import random
from rainbowtable import RainbowTable
from algorithm import Algorithm

def test_init():
    test_table = RainbowTable("sha1", "alphanumeric", 1, 1, 1, 1)
    assert test_table.config is not None
    assert test_table.algorithm == Algorithm.SHA1
    assert test_table.charset == "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    with pytest.raises(ValueError):
        test_table = RainbowTable("sha1000", "alphanumeric", 1, 1, 1, 1)
    with pytest.raises(ValueError):
        test_table = RainbowTable("sha1", "charsetnotfound", 1, 1, 1, 1)


def test_hash_function():
    test_table = RainbowTable("sha1", "alphanumeric", 1, 1, 1, 1)
    assert test_table.hash_function("rainbowtable").hex(
    ) == "ec44b366a89bb2ba78d6b8e5e81194d596d301b7"
    test_table = RainbowTable("md5", "alphanumeric", 1, 1, 1, 1)
    assert test_table.hash_function(
        "rainbowtable").hex() == "c055588e18df56f877f3c3ca73790ecd"


def test_reduce_function():
    test_table = RainbowTable("sha1", "alphanumeric", 4, 7, 1, 1)
    for i in range(50):
        randomstring = ''.join(random.choices(string.ascii_lowercase, k=5))
        hashstring = test_table.hash_function(randomstring)
        reduced = test_table.reduce_function(hashstring, i)
        assert set(reduced) <= set(test_table.charset)
        assert len(reduced) in range(4, 8)


def test_generate_table():
    test_table = RainbowTable("sha1", "alphanumeric", 2, 4, 5, 30)
    test_table.generate_table()
    first_chain = test_table.table.popitem()
    assert len(first_chain[0]) == 20
    assert len(first_chain[1]) in range(2, 5)


def test_save_and_load(tmpdir):
    test_table = RainbowTable("sha1", "alphanumeric", 2, 4, 5, 10)
    test_table.generate_table()
    test_table.save_to_file(str(tmpdir) + "/newSerializedTable.rt")
    sameTable = RainbowTable.load_from_file(
        str(tmpdir) + "/newSerializedTable.rt")
    assert test_table.table == sameTable.table


def test_lookup():
	test_table = RainbowTable.load_from_file("test/mocktable.ttest")
	psw = test_table.lookup(
		"e4815b09a6fdc84943f727b1611bd704899864ca"
	)
	assert psw == "cUK"
