#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python port of client.perl

import xmlrpclib
import datetime

url = "http://localhost:2001/RPC2?src=en;tgt=zh"
proxy = xmlrpclib.ServerProxy(url)

text = u"hey play boy ."
params = {"text":text, "align":"true", "report-all-factors":"true"}

result = proxy.translate(params)

print result

'''if 'id' in result:
    print "Segment ID:%s" % (result['id'])

if 'align' in result:
    print "Phrase alignments:"
    aligns = result['align']
    for align in aligns:
        print "%s,%s,%s" %(align['tgt-start'], align['src-start'], align['src-end'])'''