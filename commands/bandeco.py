#!/usr/bin/env python2
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

import json
import urllib2

def command_bandeco(bot):
    bandeco_url = \
        "http://www.students.ic.unicamp.br/~ra091187/bandeco_svg/json.php"

    try:
        u = urllib2.urlopen(bandeco_url, timeout = 5)
        st = u.read()
    except urllib2.URLError:
        return "Indisponível :("

    st = st[len("bandeco("):-2]

    d = json.loads(st, encoding = "latin-1")
    d.update((k, v.strip().lower()) for k, v in d.items())

    bandeco_str = \
        "%(prato)s, com suco de %(suco)s, " \
        "salada %(salada)s e sobremesa %(sobremesa)s." % d

    bandeco_str = bandeco_str[0].upper() + bandeco_str[1:]
    return bandeco_str.encode("utf-8")

command_description = [("bandeco", command_bandeco, ("bandejão",))]
