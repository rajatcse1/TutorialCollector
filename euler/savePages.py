import urllib2,cookielib
import bs4
import sys
import os

if os.path.exists("output.html"):
    os.remove("output.html")

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

# https://projecteuler.net/problem=601
count = 559
total = 601
# paragraphs = []
while (count <= 601):
    sys.stdout.write('\r' + "LOADING : (" + str(count) + "/" + str(total) + ")")
    sys.stdout.flush()
    req = urllib2.Request('https://projecteuler.net/problem='+str(count), headers=hdr)
    page = urllib2.urlopen(req)
    soup = bs4.BeautifulSoup(page.read(), 'html.parser')
    content = soup.select("div#content")
    # paragraphs.append(content[0].encode('utf-8'))
    with open('questions/Q'+ format(count,'04') +'.html', 'a') as fid:
        fid.write(content[0].encode('utf-8'))
    count = count + 1
print "Done!."