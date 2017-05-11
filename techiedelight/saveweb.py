import urllib2,cookielib
import bs4
import sys
import os
import json

# declaration
states = {}
states['id'] = 'Tutorial_Salesforce_Developer_Beginner'
routes = []

if os.path.isfile("output.html"):
	os.remove("output.html")
if os.path.isfile("bookmark.html"):
	os.remove("bookmark.html")

filelist = [ f for f in os.listdir("./app/pages")]
for f in filelist:
    os.remove("./app/pages/"+f)

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
req = urllib2.Request('https://trailhead.salesforce.com/trails/force_com_dev_beginner', headers=hdr)
page = urllib2.urlopen(req)
soup = bs4.BeautifulSoup(page.read(), 'html.parser')
modules = soup.select('.trail-module-item')
for module in modules:
	moduleName = module.select('.module-title a')[0].contents[0].encode('utf-8')
	links = module.select("div.module-content a.trailhead-item-link")
	for link in links:
		linkName = link.contents[0].encode('utf-8').replace('\n','')
		linkUrl = str(link['href'])
		subUrl = linkUrl.rsplit('/', 1)[1]

		route = {}
		route['name'] = linkName
		route['moduleName'] = moduleName
		route['url'] = "/"+subUrl
		route['templateUrl'] = "./pages/"+ subUrl +".html"
		routes.append(route)
# print links
states["routes"] = routes
if os.path.isfile("app/states.json"):
	os.remove("app/states.json")
with open('app/states.json', 'a') as fid:
	fid.write(json.dumps(states))
print "'app/states.json' file created !!!"
# Print Content
links = soup.select("div.module-content a.trailhead-item-link")

total = len(links)
current = 0
for a in links:
	current = current + 1
	sys.stdout.write('\r' + "LOADING : [" + (current * '-') + ">" + ((total-current) * ' ') + "]")
	sys.stdout.write("LOADING : (" + str(current) + "/" + str(total) + ")")
	sys.stdout.flush()

	try:
		url = "https://trailhead.salesforce.com/" + str(a['href'])
		req = urllib2.Request(url, headers=hdr)
		page = urllib2.urlopen(req)
		soup = bs4.BeautifulSoup(page.read(), 'html.parser')
		
		paragraphs = []

		# topic = soup.select("div.dropdown-link-container h1")
		# paragraphs.append(topic[0].encode('utf-8'))

		content = soup.select("div.unit-content")
		paragraphs.append(content[0].encode('utf-8'))

		subUrl = str(a['href']).rsplit('/', 1)[1]
		with open('app/pages/'+ subUrl +'.html', 'a') as fid:
			fid.write(''.join(paragraphs))
	except:
		print "loading failed:" + str(a['href'])
print "\nDone!."

