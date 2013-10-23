# -*- coding: utf8 -*-

import unittest
import bcode


# --------------
#    TESTING
# --------------

class TestEncoding(unittest.TestCase):
    def setUp(self):
        pass

    # STRINGS
    def test_encode_string(self):
        self.assertEqual(bcode.bencode('spam'), '4:spam')

    def test_encode_unicode_string_1(self):
        self.assertEqual(bcode.bencode(u'eggs'), '4:eggs')

    def test_encode_unicode_string_2(self):
        self.assertEqual(bcode.bencode(u'pão'), '4:p\xc3\xa3o')

    # INTEGERS
    def test_encode_integer(self):
        self.assertEqual(bcode.bencode(3), 'i3e')

    # FLOATS
    def test_encode_float(self):
        self.assertEqual(bcode.bencode(3.3), '3:3.3')

    # ITERABLES
    def test_encode_list(self):
        self.assertEqual(bcode.bencode(['spam', 'eggs']), 'l4:spam4:eggse')

    def test_encode_tuple(self):
        self.assertEqual(bcode.bencode((1, 2)), 'li1ei2ee')

    def test_encode_xrange(self):
        self.assertEqual(bcode.bencode(xrange(1, 6)), 'li1ei2ei3ei4ei5ee')

    def test_encode_list_in_list(self):
        self.assertEqual(bcode.bencode(['spam', ['a', 'b']]), 'l4:spaml1:a1:bee')

    def test_encode_dict_two_members(self):
        self.assertEqual(bcode.bencode({'cow': 'moo', 'spam': 'eggs'}),
                         'd3:cow3:moo4:spam4:eggse')

    def test_encode_list_in_dict(self):
        self.assertEqual(bcode.bencode({'spam': ['a', 'b']}), 'd4:spaml1:a1:bee')

    def test_encode_dict_in_dict(self):
        self.assertEqual(bcode.bencode({'fruit': {'a': 'apple', 'b': 'banana'},
                                  'cow': 'moo'}),
                         'd5:fruitd1:a5:apple1:b6:bananae3:cow3:mooe')


class TestDecoding(unittest.TestCase):
    def setUp(self):
        pass

    # INTEGERS
    def test_decode_single_integer(self):
        self.assertEqual(bcode.bdecode('i3e'), 3)

    # FLOATS
    def test_decode_single_float(self):
        self.assertEqual(bcode.bdecode('3:3.3'), '3.3')

    # STRINGS
    def test_decode_single_string_1(self):
        self.assertEqual(bcode.bdecode('4:spam'), 'spam')

    def test_decode_single_string_2(self):
        self.assertEqual(bcode.bdecode('13:spam and eggs'), 'spam and eggs')

    def test_decode_single_unicode_string(self):
        self.assertEqual(u'pão'.encode('utf-8'), bcode.bdecode('4:p\xc3\xa3o'))

    def test_decode_short_string(self):
        self.assertEqual(' egg', bcode.bdecode('4: egg'))

    # LISTS
    def test_decode_single_list(self):
        self.assertEqual(bcode.bdecode('l4:spam4:eggse'), ['spam', 'eggs'])

    def test_decode_list_in_list(self):
        self.assertEqual(bcode.bdecode('l4:spaml1:a1:bee'), ['spam', ['a', 'b']])

    def test_decode_dicts_in_list(self):
        self.assertEqual(bcode.bdecode('ld1:ai1e1:bi2eed1:ci3e1:di4eee'),
                         [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}])

    # DICTS
    def test_decode_single_dict(self):
        self.assertEqual(bcode.bdecode('d3:cow3:moo4:spam4:eggse'),
                         {'cow': 'moo', 'spam': 'eggs'})

    def test_decode_list_in_dict(self):
        self.assertEqual(bcode.bdecode('d4:spaml1:a1:bee'), {'spam': ['a', 'b']})

    def test_decode_dict_in_dict(self):
        self.assertEqual(bcode.bdecode('d4:spamd1:a1:bee'), {'spam': {'a': 'b'}})

    # MULTIPLE TYPES
    def test_decode_complex_1(self):
        self.assertEqual(bcode.bdecode('d4:teamld4:name3:bob3:agei30e6:skillsl6:python4:htmleed4:name5:jimmy3:agei32e6:skillsleeee'),
                         {'team': [{'skills': ['python', 'html'], 'age': 30, 'name': 'bob'}, {'skills': [], 'age': 32, 'name': 'jimmy'}]})


# https://github.com/cristianav/PyBencoder

"""
    bcode encodes ascii data into utf-8 and passes back the byte string
    obviously disagreeing with the spec interpretation for bencode

    bcode raises exceptions because "Errors should never pass silently." - pep20
"""

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


# https://github.com/flying-sheep/bcode

#basic en/decoding

def test_stream_decoding():
    with BytesIO(b'd2:hii1ee') as f:
        mapping = bdecode(f)
    assert mapping['hi'] == 1


def test_buffer_decoding():
    assert bdecode(b'3:one') == 'one'
    assert bdecode('3:two') == 'two'


def test_stream_encoding():
    with BytesIO() as stream:
        bencode({'a': 0}, stream)
        assert stream.getvalue() == b'd1:ai0ee'


def test_buffer_encoding():
    assert bencode(('a', 0)) == b'l1:ai0ee'


#decode incomplete stuff

def test_decode_incomplete_int():
    with raises(ValueError):
        print(bdecode('i1'))


def test_decode_incomplete_buffer():
    with raises(ValueError):
        bdecode('1:')


def test_decode_incomplete_list():
    with raises(TypeError):
        print(bdecode('l'))


def test_decode_incomplete_dict():
    with raises(TypeError):
        print(bdecode('d1:k'))


if __name__ == '__main__':
    unittest.main()
