import sys
sys.path.insert(0,"../")

import unittest
import pytest

import sourkraut.frequency as freq

ampFile = "data/amplitudes.txt"
sampFile = "data/samples.txt"

# Store results from frequency check
results = freq.freqCheck(ampFile,sampFile,False)

def test_configs():
    configs = results["configs"]
    expect = ["00","01","10","11"]
    assert configs == expect

def test_actual_count():
    actualFreq = results["actualFreq"]
    expect = [1,3,2,2]
    assert actualFreq == expect

def test_expected_count():
    actualFreq = results["expectedFreq"]
    expect = [2,2,2,2]
    assert actualFreq == expect

if __name__ == "__main__":
    unittest.main()
