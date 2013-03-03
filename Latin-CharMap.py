#!python

import struct


f = open('Latin-CharMap.txt', 'wb')

#
# Single byte characters
#

f.write(u'   0 1 2 3 4 5 6 7 8 9 A B C D E F\n'.encode('ascii'))
for c in xrange(0x20, 0x100, 0x10):
    f.write((u'%02X' % c).encode('ascii'))
    for cc in xrange(c, c + 16):
        f.write(struct.pack('BB', 0x20, cc))
    f.write(struct.pack('B', 0xa))
