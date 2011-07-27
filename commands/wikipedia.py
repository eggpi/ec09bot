#-*- coding: utf-8 -*-

# Copyright (C) 2011 by Guilherme Pinto Gonçalves

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Most of the coolnes in this command comes from http://dgl.cx/wikipedia-dns

import re
import sys
import struct
import dns.resolver

try:
    import dns
except ImportError:
    print >>sys.stderr, "This bot requires dnspython."
    print >>sys.stderr, "http://www.dnspython.org/"
    raise

def normalize_unicode_chars(text):
    # The DNS query returns utf-8 encoded strings in
    # which non-ascii bytes are represented as escaped decimals.
    # So, for instance, 'text' might contain '\195\167', which
    # we must translate into the hexadecimal form '\xc3\xa7',
    # which decodes into u'\xe7' with utf-8, which means ç.
    # Here's how it happens: the sequences of escaped decimals
    # are found using a regular expession. These sequences are fed
    # into a function that does the actual conversion to the hex
    # form by packing them with struct.pack(). This packed version
    # replaces the original string.
    # There MUST be a better way to do this, and I'd love to hear
    # about it.
    def convert_decimal_codes_to_utf8(match):
        fmt = ""
        codes = list()

        for char in filter(None, match.group().split("\\")):
            fmt += "B"
            codes.append(int(char))

        return struct.pack(fmt, *codes)

    return re.sub(r'(\\\d{1,3})+', convert_decimal_codes_to_utf8, text)

def fix_breaks(text, at = 255, size = 3):
    # The text in the DNS query is broken in double-quoted
    # strings separated by a space every 'at' characters.
    # Fix this here by joining the strings.

    ret = ""
    i = 0
    for j in xrange(at, len(text), at):
        ret += text[i:j]
        i = j + size

    ret += text[i:]
    return ret

def unescape_quotes(text):
    return re.sub(r'\\"', '"', text)

def command_wikipedia(bot, arg1, *args):
    args = (arg1,) + args # Cheap trick to require at least one arg
    addr = "_".join(args) + ".wp.dg.cx"

    try:
        ans = dns.resolver.query(addr, "TXT")
    except dns.resolver.NXDOMAIN:
        return "Article not found!"
    except dns.resolver.Timeout:
        return "Unavailable :("

    text = str(ans.rrset[0]).strip('"')
    text = normalize_unicode_chars(text)
    text = unescape_quotes(text)
    text = fix_breaks(text)

    return text

command_description = [("wikipedia", command_wikipedia, ("wiki",))]
