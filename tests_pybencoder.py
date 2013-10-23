#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://github.com/cristianav/PyBencoder

"""
    bcode encodes ascii data into utf-8 and passes back the byte string
    obviously disagreeing with the spec interpretation for bencode

    bcode raises exceptions because "Errors should never pass silently." - pep20
"""

import unittest

import os
import sys

import bcode


class MockPyBencoder(object):
    def encode(self, arg=None):
        return bcode.bencode(arg)

    def decode(self, arg=None):
        return bcode.bdecode(arg)


class PyBencoderTests(unittest.TestCase):
    ''' A test class for PyBencoder class '''

    def setUp(self):
        self.bencoder = MockPyBencoder()

    def testEncodeNoInputData(self):
        self.assertEqual(self.bencoder.encode(), None)

    def testEncodeIntegerInput(self):
        self.assertEqual(self.bencoder.encode(123), "i123e")

    def testEncodeIntegerInputNegative(self):
        self.assertEqual(self.bencoder.encode(-123), "i-123e")

    def testEncodeStringInput(self):
        self.assertEqual(self.bencoder.encode("123"), "3:123")

    def testEncodeStringNoASCIIData(self):
        # self.assertEqual(self.bencoder.encode('şţoâîăăşâß'), None)
        pass

    def testEncodeIntegerZero(self):
        self.assertEqual(self.bencoder.encode(0), "i0e")

    def testDecodeNoInput(self):
        self.assertEqual(self.bencoder.decode(), None)

    def testDecodeIntegerValidInput(self):
        self.assertEqual(self.bencoder.decode('i123e'), 123)

    def testDecodeIntegerInvalidInput(self):
        #self.assertEqual(self.bencoder.decode('i12asd3e'), None)
        self.assertRaises(ValueError)

    def testDecodeStringValidInput(self):
        self.assertEqual(self.bencoder.decode('3:red'), 'red')

    def testDecodeStringInvalidInput(self):
        #self.assertEqual(self.bencoder.decode('3:re'), None)
        self.assertRaises(ValueError)

    def testEncodeEmptyList(self):
        self.assertEqual(self.bencoder.encode([]), "le")

    def testEncodeValidSimpleList(self):
        self.assertEqual(self.bencoder.encode([1, 2, 'string']), 'li1ei2e6:stringe')

    def testEncodeValidComplexList(self):
        self.assertEqual(self.bencoder.encode([1, 2, [3, 4]]), 'li1ei2eli3ei4eee')

    def testEncodeNotAllowedType(self):
        #unknown_type = unicode
        #self.assertEqual(self.bencoder.encode(unknown_type), None)
        pass

if __name__ == '__main__':
    #unittest.main()

    #suite = unittest.TestSuite()
    #suite.addTest(BenIntTest("testEncodeNoInputData"))

    suite = unittest.TestLoader().loadTestsFromTestCase(PyBencoderTests)
    unittest.TextTestRunner(verbosity=3).run(suite)
