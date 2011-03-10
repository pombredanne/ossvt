from glob import glob
from configobj import ConfigObj
import urllib2
from urllib import urlencode
from re import compile
from natsort import *
import os, sys

def packages():
    'Check config files in ./pkgs and parse the data'
    path = os.path.split(os.path.abspath(__file__))[0]
    pkg_dir = path + '/pkgs'
    packages = []
    for _file in glob("%s/*.conf" % pkg_dir):
        c = ConfigObj(_file)
        if not c['enabled'] in [True, 'True', 'true', 1, '1']:
            continue
        packages.append(c)
    return packages

def package(pkg):
    'Check config files in ./pkgs and parse the data'
    path = os.path.split(os.path.abspath(__file__))[0]
    pkg_dir = path + '/pkgs'
    package = []
    for _file in glob("%s/%s.conf" % (pkg_dir, pkg)):
        c = ConfigObj(_file)
        if not c['enabled'] in [True, 'True', 'true', 1, '1']:
            continue
        package.append(c)
    return package

def latest(p):
    'Using the data from package() or packages() check source'
    request = urllib2.Request(p['url'])
    try:
        post = {p['post_value']: p['post_data']}
    except KeyError:
        pass
    else:
        request.add_data(urlencode(post))

    content = urllib2.urlopen(request).read()
    versions = compile(p['regex']).findall(content)
    # simple sorted does not work with versions containing
    # more than one decimal
    #version = sorted(versions, reverse=True)[0]
    versions = natsorted(versions)
    versions.reverse()
    version = versions[0]
    return version
