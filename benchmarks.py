import timeit

common_setup = """
test_decoding = 'd4:teamld4:name3:bob3:agei30e6:skillsl6:python4:htmleed4:name5:jimmy3:agei32e6:skillsleeee'
test_simple_decoding = '4:spam'
test_dict = {'fruit': {'a': 'apple', 'b': 'banana'}, 'cow': 'moo'}
test_simple_dict = {'cow': 'moo', 'spam': 'eggs'}
"""

# the following two lines should be changed to test other libraries
bcode_setup = 'from bcode import bdecode\n'
bcode_setup += 'from bcode import bencode\n'
bcode_setup += common_setup

print timeit.timeit('bdecode(test_decoding)', setup=bcode_setup, number=10000)
print timeit.timeit('bdecode(test_simple_decoding)', setup=bcode_setup, number=10000)
print timeit.timeit('bencode(test_dict)', setup=bcode_setup, number=10000)
print timeit.timeit('bencode(test_simple_dict)', setup=bcode_setup, number=10000)
