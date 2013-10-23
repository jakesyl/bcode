# -*- coding: utf8 -*-

import unittest
from bcode import *


# --------------
#    TESTING
# --------------

class TestEncoding(unittest.TestCase):
    def setUp(self):
        pass

    # STRINGS
    def test_encode_string(self):
        self.assertEqual(bencode('spam'), '4:spam')

    def test_encode_unicode_string_1(self):
        self.assertEqual(bencode(u'eggs'), '4:eggs')

    def test_encode_unicode_string_2(self):
        self.assertEqual(bencode(u'pão'), '4:p\xc3\xa3o')

    # INTEGERS
    def test_encode_integer(self):
        self.assertEqual(bencode(3), 'i3e')

    # FLOATS
    def test_encode_float(self):
        self.assertEqual(bencode(3.3), '3:3.3')

    # ITERABLES
    def test_encode_list(self):
        self.assertEqual(bencode(['spam', 'eggs']), 'l4:spam4:eggse')

    def test_encode_tuple(self):
        self.assertEqual(bencode((1, 2)), 'li1ei2ee')

    def test_encode_xrange(self):
        self.assertEqual(bencode(xrange(1, 6)), 'li1ei2ei3ei4ei5ee')

    def test_encode_list_in_list(self):
        self.assertEqual(bencode(['spam', ['a', 'b']]), 'l4:spaml1:a1:bee')

    def test_encode_dict_two_members(self):
        self.assertEqual(bencode({'cow': 'moo', 'spam': 'eggs'}),
                         'd3:cow3:moo4:spam4:eggse')

    def test_encode_list_in_dict(self):
        self.assertEqual(bencode({'spam': ['a', 'b']}), 'd4:spaml1:a1:bee')

    def test_encode_dict_in_dict(self):
        self.assertEqual(bencode({'fruit': {'a': 'apple', 'b': 'banana'},
                                  'cow': 'moo'}),
                         'd5:fruitd1:a5:apple1:b6:bananae3:cow3:mooe')


class TestDecoding(unittest.TestCase):
    def setUp(self):
        pass

    # INTEGERS
    def test_decode_single_integer(self):
        self.assertEqual(bdecode('i3e'), 3)

    # FLOATS
    def test_decode_single_float(self):
        self.assertEqual(bdecode('3:3.3'), '3.3')

    # STRINGS
    def test_decode_single_string_1(self):
        self.assertEqual(bdecode('4:spam'), 'spam')

    def test_decode_single_string_2(self):
        self.assertEqual(bdecode('13:spam and eggs'), 'spam and eggs')

    def test_decode_single_unicode_string(self):
        self.assertEqual('p\xe3o', bdecode('6:p\xe3o'))

    def test_decode_short_string(self):
        self.assertEqual('egg', bdecode('4:egg'))

    # LISTS
    def test_decode_single_list(self):
        self.assertEqual(bdecode('l4:spam4:eggse'), ['spam', 'eggs'])

    def test_decode_list_in_list(self):
        self.assertEqual(bdecode('l4:spaml1:a1:bee'), ['spam', ['a', 'b']])

    def test_decode_dicts_in_list(self):
        self.assertEqual(bdecode('ld1:ai1e1:bi2eed1:ci3e1:di4eee'),
                         [{'a': 1, 'b': 2}, {'c': 3, 'd': 4}])

    # DICTS
    def test_decode_single_dict(self):
        self.assertEqual(bdecode('d3:cow3:moo4:spam4:eggse'),
                         {'cow': 'moo', 'spam': 'eggs'})

    def test_decode_list_in_dict(self):
        self.assertEqual(bdecode('d4:spaml1:a1:bee'), {'spam': ['a', 'b']} )

    def test_decode_dict_in_dict(self):
        self.assertEqual(bdecode('d4:spamd1:a1:bee'), {'spam': {'a': 'b'}})

    # MULTIPLE TYPES
    def test_decode_complex_1(self):
        self.assertEqual(bdecode('d4:teamld4:name3:bob3:agei30e6:skillsl6:python4:htmleed4:name5:jimmy3:agei32e6:skillsleeee'), {'team': [{'skills': ['python', 'html'], 'age': 30, 'name': 'bob'}, {'skills': [], 'age': 32, 'name': 'jimmy'}]})

if __name__ == '__main__':
    unittest.main()