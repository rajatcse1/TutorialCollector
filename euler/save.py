import urllib2,cookielib
import bs4
import sys
import os

os.remove("output.html")
os.remove("bookmark.html")

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
req = urllib2.Request('https://trailhead.salesforce.com/trails/force_com_dev_intermediate', headers=hdr)
page = urllib2.urlopen(req)
soup = bs4.BeautifulSoup(page.read(), 'html.parser')
links = soup.select("div.module-content a.trailhead-item-link")
total = len(links)
current = 0
# print links
for a in links:
	current = current + 1
	# print "LOADING : (" + str(current) + "/" + str(total) + ")\r"
	sys.stdout.write('\r' + "LOADING : (" + str(current) + "/" + str(total) + ")")
	sys.stdout.flush()

	# print str(a['href'])
	url = "https://trailhead.salesforce.com/"+str(a['href'])
	req = urllib2.Request(url, headers=hdr)
	page = urllib2.urlopen(req)
	soup = bs4.BeautifulSoup(page.read(), 'html.parser')
	
	paragraphs = []

	topic = soup.select("div.dropdown-link-container h1")
	paragraphs.append(topic[0].encode('utf-8'))

	content = soup.select("div.unit-content")
	paragraphs.append(content[0].encode('utf-8'))

	# print "Writing Content ...."
	# sys.stdout.flush()
	with open('output.html', 'a') as fid:
		fid.write(''.join(paragraphs))
	
	paragraphs = []
	trail = soup.select("a.trail span")
	paragraphs.append(trail[0].encode('utf-8'))
	
	module = soup.select("a.module span")
	paragraphs.append(module[0].encode('utf-8'))
	
	topic = soup.select("div.dropdown-link-container h1")
	paragraphs.append(topic[0].encode('utf-8'))
	
	content = soup.select("div.sidebar-content ul")
	paragraphs.append(content[0].encode('utf-8'))

	# print "Writing Bookmarks ...."
	# sys.stdout.flush()
	with open('bookmark.html', 'a') as fid:
		fid.write(''.join(paragraphs))
	# print "------------------------------------------------"
print "Done!."