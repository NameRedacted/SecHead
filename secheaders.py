
import urllib2
import json
import sys
import re
import os

json_document = "secheaders.json"

if not os.path.isfile(json_document):
    raise Exception("Missing a required file: '%s'" % (json_document))

class Request_Handler(object):
    def __init__(self, url=None, start=False, debug=False):
        self.debug = debug
        self.start = start
        self.url = str(url)
        self.json = None
        self.headers = None
        self.content = None

        with open(json_document) as _d:
            self.json = json.load(_d)

        if self.url and self.start:
            self.headers, self.content = self.getData

    # Global getter
    def get(self, item):
        if not hasattr(self, item):
            return
        return getattr(self, item)


    # Get site content from most recent request
    @property
    def getContent(self):
        if self.content:
            return self.content


    # Extract headers and content from recent request
    @property
    def getData(self):
        if not self.url: return
        try:
            r = urllib2.urlopen(urllib2.Request(self.url))
        except urllib2.URLError, e:
            raise Exception(e.reason)
        except urllib2.HTTPError, e:
            raise Exception(e.code)
        except ValueError, e:
            raise Exception(e.message)
        except Exception:
            import traceback
            raise Exception('%s' % (traceback.format_exc()))
        return r.headers, r.read()


    # Get the headers from the most recent request
    @property
    def getHeaders(self):
        if self.headers:
            return self.headers


    # Global setter
    def set(self, item, value):
        if not hasattr(self, item):
            return
        setattr(self, item, value)


    def parseHeaders(self):
        if not self.headers: return
        hname = None
        regex = None

        for head in self.headers:
            if head in self.json.keys():
                hname = self.json[head][0]['name']
                regex = self.json[head][0]['regex']

                m = re.match(regex, self.headers[head])
                if m:
                    count = m.groups()
                    print count
