About
-----

bcode is a pair of functions that provide bencoding and bdecoding functionalities.

bencode is the format used for .torrent BitTorrent files [1]

Installation
------------

cd into the desired lib directory and type

    wget https://github.com/medecau/bcode/raw/master/bcode.py

or manually download it to the desired destination

Basic Usage
-----------

    import bcode

or if you only need to read or write

    from bcode import bdecode

    from bcode import bencode

then you can

    bencode('string')

    bencode(2010)

    bencode(['apples', 'oranges', 'bananas'])

    bencode({'name': 'jimmy', 'age': 45})

or

    bdecode('3:car')

    bdecode('i42e')

    bdecode('li10ei20ei30ee')

    bdecode('d5:color3:red4:kind3:hote')

or look at test.py to have an idea of what these functions can do.

LICENSE
-------

bcode is released under the MIT License. http://www.opensource.org/licenses/mit-license.php


.. _[1]: http://wiki.theory.org/BitTorrentSpecification#bencoding
