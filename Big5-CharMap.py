#!python

import struct


f = open('Big5-CharMap.txt', 'wb')

#
# Single byte characters
#

f.write(u'   0 1 2 3 4 5 6 7 8 9 A B C D E F\n'.encode('ascii'))
for c in xrange(0x20, 0x80, 0x10):
    f.write((u'%02X' % c).encode('ascii'))
    for cc in xrange(c, c + 16):
        if 0x7f <= cc:
            cc = 0x20
        f.write(struct.pack('BB', 0x20, cc))
    f.write(struct.pack('B', 0xa))

f.write(struct.pack('B', 0xa))


#
# Double byte characters
#

NOCHAR_RANGES = [
    (0xa3c0, 0xa3ff),
    (0xf9d6, 0xf9ff),
]

NOCHAR = set()
for a, b in NOCHAR_RANGES:
    for c in xrange(a, b+1):
        NOCHAR.add(c)

f.write(u'     _0 _1 _2 _3 _4 _5 _6 _7 _8 _9 _A _B _C _D _E _F\n'.encode('ascii'))

for ch in xrange(0xa1, 0xfa):
    if ch == 0xc7 or ch == 0xc8:
        continue
    for cl in xrange(0x40, 0x100, 0x10):
        if cl == 0x80 or cl == 0x90:
            continue
        if ch == 0xa3 and cl >= 0xc0:
            continue
        if ch == 0xc6 and cl >= 0x80:
            continue
        if ch == 0xf9 and cl >= 0xe0:
            continue
        c = (ch << 8) + cl
        f.write((u'%04X' % c).encode('ascii'))
        for cc in xrange(c, c + 16):
            if (cc & 0xff) in [ 0x7f, 0xa0, 0xff ] or cc in NOCHAR:
                cc = 0xa140
            f.write(struct.pack('>BH', 0x7c, cc))
        f.write(struct.pack('BB', 0x7c, 0xa))

