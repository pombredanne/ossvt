from urllib import urlencode
import urllib2
from re import compile

def ius_version(name):
    'Takes the results of each object of all_latest() and gets IUS version'
    request = urllib2.urlopen('http://dl.iuscommunity.org/pub/ius/stable/Redhat/5/SRPMS/')
    content = request.read()
    match = compile(name + '-([0-9.]*)-.*.src.rpm').findall(content)
    ius_ver = sorted(match, reverse=True)[0]
    return ius_ver

def compare_to_ius_simple(ius_ver, upstream_ver):
    if ius_ver < upstream_ver:
        return upstream_ver

def compare_to_ius(ius_ver, upstream_ver):
    ius_ver_split = ius_ver.split('.')
    upsteram_ver_split = upstream_ver.split('.')
    count = 0
    for i in upsteram_ver_split:
        if ius_ver_split[count] == upsteram_ver_split[count]:
            count += 1
            continue
        else:
            if int(ius_ver_split[count]) < int(upsteram_ver_split[count]):
                return upstream_ver
            else:
                break