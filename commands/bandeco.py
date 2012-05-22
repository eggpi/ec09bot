#-*- coding: utf-8 -*-

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
