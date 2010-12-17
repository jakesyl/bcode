About
-----

bcode is a pair of functions that provide bencoding and bdecoding functionalities.

bencode is the format used for .torrent BitTorrent files [1]_

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

LICENSE
-------

bcode is released under the MIT License. http://www.opensource.org/licenses/mit-license.php


.. _[1]: http://wiki.theory.org/BitTorrentSpecification#bencoding
