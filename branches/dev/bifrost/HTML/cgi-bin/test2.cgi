#!C:\Python27\python.exe -u
#!/usr/bin/env python

import cgi
import cgitb; cgitb.enable()  # for troubleshooting

print "Content-type: text/html"
print

print """
<html>

<head><title>Sample CGI Script</title></head>

<body>

  <h3> Sample CGI Script </h3>
"""

form = cgi.FieldStorage()
input = form.getvalue("InputName", "(no message)")
market = form.getvalue("MarketName", "(no message)")
others = form.getvalue("OtherFields", "(no message)")

print """<p>Stock Ticker: %s</p>""" % cgi.escape(input)


print """<p>Market Name Ticker: %s</p>""" % cgi.escape(market)

count = 0
for i in others:
    count+=1
    print "<p>Field ",
    print count,
    print ": %s</p>"% cgi.escape(i)


print """
</body>
</html>
"""
