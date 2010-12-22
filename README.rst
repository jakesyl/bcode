About
-----

bcode is a pair of functions that provide bencoding and bdecoding functionalities.

bencode is the format used to store data in .torrent BitTorrent files [1]_

Installation
------------

bcode is available through PyPI: 

    easy_install bcode

but if you prefer to do it manually you can download and unpack from:

    https://github.com/medecau/bcode/tarball/master

cd into the unpacked directory and:

    python setup.py install


Basic Usage
-----------

    import bcode

or if you only need to read or write

    from bcode import bdecode

    from bcode import bencode

then you can pass it strings, integers, lists and dictionaries

    bencode('string')

    bencode(2010)

    bencode(['apples', 'oranges', 'bananas'])

    bencode({'name': 'jimmy', 'age': 45})

or encoded strings

    bdecode('3:car')

    bdecode('i42e')

    bdecode('li10ei20ei30ee')

    bdecode('d5:color3:red4:kind3:hote')

or look at test.py to have an idea of what these functions can do.

Notes
_____

When encoding:
Lists and dictionaries can contain strings, integers, lists and dictionaries has values.
Dictionary keys must be strings.

When decoding
Fields always start with an 'i', an 'l', a 'd' or a decimal number.
Integers, lists and dictionaries end with an 'e', the starting decimal number in strings defines their length.

Learn more about bencode and bittorrent at: http://wiki.theory.org/BitTorrentSpecification#bencoding

LICENSE
-------

bcode is released under the MIT License. http://www.opensource.org/licenses/mit-license.php


.. _[1]: http://wiki.theory.org/BitTorrentSpecification#bencoding
