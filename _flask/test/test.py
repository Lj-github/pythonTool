"""
Copyright © 2014 Eduard Tomasek <???>
This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See the COPYING file for more details.
"""

import json
import _flask.lib.lzstring as lzstring
import pprint
x = lzstring.LZString()

if __name__ == '__main__':

    s = 'aaaaaa!'
    print('String for encode: ' + s)
    print('String for encode: ' + str(len(s)) )
    print('Compress to base64:')
    base2 = x.compress(s)
    print('result:    ' + base2)
    print('String for base2: ' + str(len(base2)))
    print('Decompress from base64:')
    print('result:' + x.decompress(base2))
