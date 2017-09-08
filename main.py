#!/usr/bin/env python2

from secheaders import Request_Handler
import os

try:
    request = Request_Handler("http://google.com", True)
    request.parseHeaders()

except Exception, e:
    print "\n%s\n" % e.args[0]