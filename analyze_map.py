#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2016 Scott Shawcroft for Adafruit Industries
# Copyright (c) 2018 Ralph Versteegen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function

import sys
import os
import argparse

parser = argparse.ArgumentParser(description='Summarises the size of each object file in an ld linker map.')
parser.add_argument('map_file', help="A map file generated by passing -M/--print-map to ld during linking.")
parser.add_argument('--combine', action='store_true',
                    help="All object files in an .a archive or in a directory are combined")
args = parser.parse_args()

class SectionSize():
    code = 0
    data = 0  # Including metadata like import tables
    def total(self):
        return self.code + self.data
    def add_section(self, section, size):
        if section.startswith('.text'):
            self.code += size
        elif section != '.bss':
            self.data += size

size_by_source = {}
with open(args.map_file) as f:
    lines = iter(f)
    for line in lines:
        if line.strip() == "Linker script and memory map":
            break

    current_section = None
    split_line = None
    for line in lines:
        line = line.strip('\n')
        if split_line:
            # Glue a line that was split in two back together
            if line.startswith(' ' * 16):
                line = split_line + line
            else:  # Shouldn't happen
                print("Warning: discarding line ", split_line)
            split_line = None

        if line.startswith((".", " .", " *fill*")):
            pieces = line.split(None, 3)  # Don't split paths containing spaces

            if line.startswith("."):
                # Note: this line might be wrapped, with the size of the section
                # on the next line, but we ignore the size anyway and will ignore that line
                current_section = pieces[0]
            elif len(pieces) == 1 and len(line) > 14:
                # ld splits the rest of this line onto the next if the section name is too long
                split_line = line
            elif len(pieces) >= 3 and "=" not in pieces and "before" not in pieces:
                if pieces[0] == "*fill*":
                    source = pieces[0]
                    size = int(pieces[-1], 16)
                else:
                    source = pieces[-1]
                    size = int(pieces[-2], 16)

                if args.combine:
                    if '.a(' in source:
                        # path/to/archive.a(object.o)
                        source = source[:source.index('.a(') + 2]
                    elif source.endswith('.o'):
                        where = max(source.rfind('\\'), source.rfind('/'))
                        if where:
                            source = source[:where + 1] + '*.o'

                if source not in size_by_source:
                    size_by_source[source] = SectionSize()
                size_by_source[source].add_section(current_section, size)

# Print out summary
sources = list(size_by_source.keys())
sources.sort(key = lambda x: size_by_source[x].total())
sumtotal = sumcode = sumdata = 0
for source in sources:
    size = size_by_source[source]
    sumcode += size.code
    sumdata += size.data
    sumtotal += size.total()
    print("%-40s \t%7s  (code: %d data: %d)" % (os.path.normpath(source), size.total(), size.code, size.data))
print("TOTAL %d  (code: %d data: %d)" % (sumtotal, sumcode, sumdata))
