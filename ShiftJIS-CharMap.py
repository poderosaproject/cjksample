#!python

import struct


f = open('ShiftJIS-CharMap.txt', 'wb')

#
# Single byte characters
#

f.write(u'   0 1 2 3 4 5 6 7 8 9 A B C D E F\n'.encode('ascii'))
for c in xrange(0x20, 0x100, 0x10):
    f.write((u'%02X' % c).encode('ascii'))
    for cc in xrange(c, c + 16):
        if 0x7f <= cc <= 0xa0 or 0xe0 <= cc <= 0xff:
            cc = 0x20
        f.write(struct.pack('BB', 0x20, cc))
    f.write(struct.pack('B', 0xa))

f.write(struct.pack('B', 0xa))


#
# Double byte characters
#

NOCHAR_RANGES = [
  (0x81ad, 0x81b7),
  (0x81c0, 0x81c7),
  (0x81cf, 0x81d9),
  (0x81e9, 0x81ef),
  (0x81f8, 0x81fb),
  (0x8240, 0x824e),
  (0x8259, 0x825f),
  (0x827a, 0x8280),
  (0x829b, 0x829e),
  (0x82f2, 0x82fc),
  (0x8397, 0x839e),
  (0x83b7, 0x83be),
  (0x83d7, 0x83df),
  (0x83e0, 0x83fc),
  (0x8461, 0x846f),
  (0x8492, 0x849e),
  (0x84bf, 0x84fc),
  (0x875e, 0x875e),
  (0x8776, 0x877d),
  (0x879d, 0x87fc),
  (0x8840, 0x889e),
  (0x9873, 0x989e),
  (0xeaa5, 0xeafc),
  (0xeeed, 0xeeee),
]

NOCHAR = set()
for a, b in NOCHAR_RANGES:
    for c in xrange(a, b+1):
        NOCHAR.add(c)

f.write(u'     _0 _1 _2 _3 _4 _5 _6 _7 _8 _9 _A _B _C _D _E _F\n'.encode('ascii'))
for ch in xrange(0x81, 0xa0):
    if ch == 0x85 or ch == 0x86:
        continue
    for cl in xrange(0x40, 0x100, 0x10):
        c = (ch << 8) + cl
        f.write((u'%04X' % c).encode('ascii'))
        for cc in xrange(c, c + 16):
            if (cc & 0xff) in [ 0x7f, 0xfd, 0xfe, 0xff ] or cc in NOCHAR:
                cc = 0x8140
            f.write(struct.pack('>BH', 0x7c, cc))
        f.write(struct.pack('BB', 0x7c, 0xa))

for ch in xrange(0xe0, 0xef):
    if ch == 0xeb or ch == 0xec:
        continue
    for cl in xrange(0x40, 0x100, 0x10):
        c = (ch << 8) + cl
        f.write((u'%04X' % c).encode('ascii'))
        for cc in xrange(c, c + 16):
            if (cc & 0xff) in [ 0x7f, 0xfd, 0xfe, 0xff ] or cc in NOCHAR:
                cc = 0x8140
            f.write(struct.pack('>BH', 0x7c, cc))
        f.write(struct.pack('BB', 0x7c, 0xa))
