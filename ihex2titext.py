#!/usr/bin/env python
# simple intel hex (and elf) to TI text converter
# data is read from stdin and output on stdout
# usage: cat file.a43 | ihex2titext >out.txt
# usage: ihex2titext file.a43 >out.txt
# usage: ihex2titext file.a43 -o out.txt
#
# (C) 2005 Chris Liechti <cliechti@gmx.net>
# this is distributed under a free software license, see license.txt
#
# $Id: ihex2titext.py,v 1.3 2005/12/28 22:02:27 cliechti Exp $

from msp430 import memory
import sys

from optparse import OptionParser

parser = OptionParser(usage='usage: %prog [-o filename.txt|-] file.a43|-')
parser.add_option("-o", "--output", dest="output",
                  help="write result to given file", metavar="FILE")
(options, args) = parser.parse_args()

if not args:
    parser.error('no input files given')

#prepare output
if options.output is None or options.output == '-':
    out = sys.stdout
else:
    out = file(options.output, 'wb')

#get input
data = memory.Memory()

for filename in args:
    if filename == '-':
        data.loadIHex(sys.stdin)                #intel-hex
    else:
        data.loadFile(filename)

#output TI-Text
for segment in data:
    out.write("@%04x\n" % segment.startaddress)
    for i in range(0, len(segment.data), 16):
        out.write("%s\n" % " ".join(["%02x" % ord(x) for x in segment.data[i:i+16]]))
out.write("q\n")