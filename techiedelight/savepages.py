import urllib2,cookielib
import bs4
import sys
import os
import json

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
req = urllib2.Request('http://www.techiedelight.com/list-of-problems/', headers=hdr)
page = urllib2.urlopen(req)
soup = bs4.BeautifulSoup(page.read(), 'html.parser')
# print soup
modules = soup.select('h2.tabtitle')
# div.tabcontent
for module in modules:
    moduleName = module.contents[0].encode('utf-8')
    directoryName = 'app/pages/'+ moduleName.strip()
    if not os.path.exists(directoryName):
        os.makedirs(directoryName)
    # print directoryName
    links = module.findNext('ol').select('a')
    for link in links:
        # #post-7825 > div
        # //*[@id="post-7825"]/div
        # try:
            url = str(link['href'])
            subUrl = url.rsplit('/', 2)[1]
            # print subUrl
            req = urllib2.Request(url, headers=hdr)
            page = urllib2.urlopen(req)
            soup = bs4.BeautifulSoup(page.read(), 'html.parser')
            
            content = soup.select("html")
            # print content
            
            with open(directoryName +"/"+ subUrl +'.html', 'a') as fid:
                fid.write(content[0].encode('utf-8'))
            rajat
        # except:
        #     print "loading failed:" + str(a['href'])
        # print link['href']
