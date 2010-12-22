# -*- coding: utf-8 -*-
license = '''
Copyright (c) 2010 Pedro Rodrigues

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

'''


# ---------------
#    ENCODING
# ---------------

def _encode_string(input):
    return '%d:%s' % (len(input),input)

def _encode_integer(input):
    return 'i%de' % input

def _encode_list(input):
    result = ''
    for each in input:
        result += bencode(each)
    return 'l%se' % result

def _encode_dictionary(input):
    result = ''
    for key, value in input.iteritems():
        result += bencode(key)+bencode(value)
    return 'd%se' % result


# ---------------
#    DECODING
# ---------------

def _decode_integer(input):
    end = input.find('e')
    if end>-1:
        return (int(input[1:end]),input[end+1:])
        end += 1
    else:
        raise ValueError("Missing ending delimiter 'e'")

def _decode_string(input):
    start = input.find(':')+1
    size = int(input[:start-1])
    end = start+size
    return (input[start:end], input[end:])

def _decode_list(input):
    result = []
    remainder = input[1:]
    while True:
        if remainder[0] == 'i':
            r = _decode_integer(remainder)
            result.append(r[0])
            remainder = r[1]
        
        elif remainder[0].isdigit():
            r = _decode_string(remainder)
            result.append(r[0])
            remainder = r[1]
        
        elif remainder[0] == 'l':
            r = _decode_list(remainder)
            result.append(r[0])
            remainder = r[1]
        
        elif remainder[0] == 'd':
            r = _decode_dict(remainder)
            result.append(r[0])
            remainder = r[1]
        
        elif remainder[0] == 'e':
            remainder = remainder[1:]
            break
        
        else:
            raise ValueError("Invalid initial delimiter '%r' found while decoding a list" % remainder[0])
    
    return (result,remainder)

def _decode_dict(input):
    result = {}
    remainder = input[1:]
    while remainder[0] != 'e':
        r = _decode_string(remainder)
        key = r[0]
        remainder = r[1]
        
        if remainder[0] == 'i':
            r = _decode_integer(remainder)
            value = r[0]
            result[key] = value
            remainder = r[1]
        
        elif remainder[0].isdigit():
            r = _decode_string(remainder)
            value = r[0]
            result[key] = value
            remainder = r[1]
        
        elif remainder[0] == 'l':
            r = _decode_list(remainder)
            value = r[0]
            result[key] = value
            remainder = r[1]
        
        elif remainder[0] == 'd':
            r = _decode_dict(remainder)
            value = r[0]
            result[key] = value
            remainder = r[1]
        
        else:
            raise ValueError("Invalid initial delimiter '%r' found while decoding a dictionary" % ramainder[0])
    
    return (result,remainder[1:])


# -------------
#    PUBLIC
# -------------

def bencode(input):
    '''Encode python types to bencode format.
    
    Keyword arguments:
    input -- the input value to be encoded
    '''
    
    if type(input) == type(str()):
        return _encode_string(input)
    
    elif type(input) == type(int()):
        return _encode_integer(input)
    
    elif type(input) == type(list()):
        return _encode_list(input)
    
    elif type(input) == type(dict()):
        return _encode_dictionary(input)
    
    else:
        raise ValueError('Invalid field type: %r' % type(input))


def bdecode(input):
    '''Decode strings from bencode format to python value types.
    
    Keyword arguments:
    input -- the input string to be decoded
    '''
    
    input = input.strip()
    
    if input[0] == 'i':
        return _decode_integer(input)[0]
    
    elif input[0].isdigit():
        return _decode_string(input)[0]
    
    elif input[0] == 'l':
        return _decode_list(input)[0]

    elif input[0] == 'd':
        return _decode_dict(input)[0]
    else:
        raise ValueError("Invalid initial delimiter '%s'" % input[0])
