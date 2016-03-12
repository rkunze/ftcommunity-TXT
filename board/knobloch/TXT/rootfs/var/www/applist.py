#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

import ConfigParser
import sys, os

base = "/opt/ftc"

print '<table cellspacing="20">'

cols = 4   # 3 is same as on TXT itself
count = 0

# find all manifest files in the apps directory
for name in os.listdir(base + "/apps"):
    manifestfile = base + "/apps/" + name + "/manifest"
    if os.path.isfile(manifestfile):
        manifest = ConfigParser.RawConfigParser()
        manifest.read(manifestfile)

        # get various fields from manifest
        appname = manifest.get('app', 'name')
        description = manifest.get('app', 'desc')
        iconname = "apps/" + name + "/" + manifest.get('app', 'icon')

        if count == 0:
            print "<tr>"
            
        print '<td align="center">'
        print '<div title="' + description + '">'
        print '<img src="' + iconname + '"><br>'
        print appname + '</div></td>'

        count += 1
        if count == cols:
            print "</tr>"
            count = 0

# fill columns
while count != 0:
    print "<td></td>"
    count += 1
    if count == cols:
        print "</tr>"
        count = 0
        
print "</table>"