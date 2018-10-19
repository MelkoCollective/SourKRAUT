import sys
sys.path.insert(0,"../")

import unittest
import pytest
import math

import sourkraut.operator as oper

# Create an example amplitudes list
amps = [
    1/math.sqrt(8),
    0/math.sqrt(8),
    0/math.sqrt(8),
    4/math.sqrt(8),
    0/math.sqrt(8),
    2/math.sqrt(8),
    1/math.sqrt(8),
    0/math.sqrt(8)
]

def test_transform_1():
    state = "1010"
    newState = oper.transform(state,1,"S+S-")
    assert newState == "1100"

def test_transform_2():
    state = "1010"
    newState = oper.transform(state,2,"S-S+")
    assert newState == "1001"

def test_convert_S2S3_1():
    state = "101"
    value = oper.convert("S2S3",state,amps)
    assert value == -0.25

def test_convert_S2S3_2():
    state = "011"
    value = oper.convert("S2S3",state,amps)
    assert value == 0.25

def test_convert_SzSz_1():
    state = "101"
    value = oper.convert("SzSz",state,amps)
    assert value == -0.5

def test_convert_SzSz_2():
    state = "011"
    value = oper.convert("SzSz",state,amps)
    assert value == 0

def test_convert_SpSm_1():
    state = "101"
    value = oper.convert("S+S-",state,amps)
    assert value == 0.5

def test_convert_SpSm_2():
    state = "000"
    value = oper.convert("S+S-",state,amps)
    assert value == 0

def test_convert_SmSp_1():
    state = "101"
    value = oper.convert("S-S+",state,amps)
    assert value == 2

def test_convert_SmSp_2():
    state = "000"
    value = oper.convert("S-S+",state,amps)
    assert value == 0

listofMs = range(100,20000,100)
ampFile = "data/10Q/Amplitudes.txt"
sampFile = "data/10Q/Samples.txt"
obsFile = "data/10Q/Observables.txt"

def test_operatorCheck_1():
    error = oper.operatorCheck("H",listofMs,ampFile,sampFile,obsFile)
    assert error < 0.0001

listofMs = range(100,20000,100)
ampFile = "data/15Q/Amplitudes.txt"
sampFile = "data/15Q/Samples.txt"
obsFile = "data/15Q/Observables.txt"

def test_operatorCheck_2():
    error = oper.operatorCheck("H",listofMs,ampFile,sampFile,obsFile)
    assert error < 0.0001

listofMs = range(100,20000,100)
ampFile = "data/20Q/Amplitudes.txt"
sampFile = "data/20Q/Samples.txt"
obsFile = "data/20Q/Observables.txt"

def test_operatorCheck_3():
    error = oper.operatorCheck("H",listofMs,ampFile,sampFile,obsFile)
    assert error < 0.0001

if __name__ == "__main__":
    unittest.main()
