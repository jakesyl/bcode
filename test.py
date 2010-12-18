import unittest
from bcode import *

# --------------
#    TESTING
# --------------

class TestBcode(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_encode_string(self):
        self.assertEqual(bencode('spam'), '4:spam')
    
    def test_encode_integer(self):
        self.assertEqual(bencode(3), 'i3e')
    
    def test_encode_list(self):
        self.assertEqual(bencode(['spam', 'eggs']), 'l4:spam4:eggse')
    
    def test_encode_list_in_list(self):
        self.assertEqual(bencode(['spam', ['a', 'b']]), 'l4:spaml1:a1:bee')
    
    def test_encode_dict_two_members(self):
        self.assertEqual(bencode({'cow': 'moo', 'spam': 'eggs' }), 'd3:cow3:moo4:spam4:eggse')
    
    def test_encode_list_in_dict(self):
        self.assertEqual(bencode({'spam': [ 'a', 'b' ] }), 'd4:spaml1:a1:bee')

    def test_encode_dict_in_dict(self):
        self.assertEqual(bencode({'fruit': {'a': 'apple', 'b': 'banana'}, 'cow': 'moo'}), 'd5:fruitd1:a5:apple1:b6:bananae3:cow3:mooe')

    def test_decode_single_integer(self):
        self.assertEqual(bdecode('i3e'), 3)
    
    def test_decode_single_string(self):
        self.assertEqual(bdecode('4:spam'), 'spam')
    
    def test_decode_single_list(self):
        self.assertEqual(bdecode('l4:spam4:eggse'), ['spam', 'eggs'])
    
    def test_decode_list_in_list(self):
        self.assertEqual(bdecode('l4:spaml1:a1:bee'), ['spam', ['a', 'b']])

    def test_decode_dicts_in_list(self):
        self.assertEqual(bdecode('ld1:ai1e1:bi2eed1:ci3e1:di4eee'), [{'a': 1,'b': 2},{'c': 3,'d': 4}])
    
    def test_decode_single_dict(self):
        self.assertEqual(bdecode('d3:cow3:moo4:spam4:eggse'), {'cow': 'moo', 'spam': 'eggs' })
    
    def test_decode_list_in_dict(self):
        self.assertEqual(bdecode('d4:spaml1:a1:bee'), {'spam': [ 'a', 'b' ] })

    def test_decode_dict_in_dict(self):
        self.assertEqual(bdecode('d4:spamd1:a1:bee'), {'spam': {'a': 'b' } })

    def test_decode_complex_1(self):
        self.assertEqual(bdecode('d4:teamld4:name3:bob3:agei30e6:skillsl6:python4:htmleed4:name5:jimmy3:agei32e6:skillsleeee'), {'team':[{'skills':['python','html'], 'age':30, 'name':'bob'},{ 'skills':[], 'age':32, 'name':'jimmy'}]})

if __name__ == '__main__':
    unittest.main()