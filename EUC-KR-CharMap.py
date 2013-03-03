#!python

import struct


f = open('EUC-KR-CharMap.txt', 'wb')

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
    (0xa2e8, 0xa2ff),
    (0xa5ab, 0xa5af),
    (0xa5ba, 0xa5c0),
    (0xa5d9, 0xa5df),
    (0xa5e0, 0xa5e0),
    (0xa5f9, 0xa5ff),
    (0xa6e5, 0xa6ff),
    (0xa7f0, 0xa7ff),
    (0xa8a5, 0xa8a5),
    (0xa8a7, 0xa8a7),
    (0xa8b0, 0xa8b0),
    (0xaaf4, 0xaaff),
    (0xabf7, 0xabff),
    (0xacc2, 0xacd0),
    (0xacf2, 0xacff),
]

NOCHAR = set()
for a, b in NOCHAR_RANGES:
    for c in xrange(a, b+1):
        NOCHAR.add(c)

f.write(u'     _0 _1 _2 _3 _4 _5 _6 _7 _8 _9 _A _B _C _D _E _F\n'.encode('ascii'))

for ca, cb in [(0xa1, 0xac), (0xb0, 0xc8), (0xca, 0xfd)]:
    for ch in xrange(ca, cb+1):
        for cl in xrange(0xa0, 0x100, 0x10):
            c = (ch << 8) + cl
            f.write((u'%04X' % c).encode('ascii'))
            for cc in xrange(c, c + 16):
                if (cc & 0xff) in [ 0xa0, 0xff ] or cc in NOCHAR:
                    cc = 0xa1a1
                f.write(struct.pack('>BH', 0x7c, cc))
            f.write(struct.pack('BB', 0x7c, 0xa))

