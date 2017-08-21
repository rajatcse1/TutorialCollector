import json
import sys
import os
import urllib2

def trace( tag, message, flush=True):
	sys.stdout.write('\n'+tag+" : " + str(message)+'\n')
	if flush:
		sys.stdout.flush()
	return

def progressbar(current, total):
	sys.stdout.write("\r%d / %d" %(current, total))
	# sys.stdout.write("\r[%-20s] %d%%" % ('='*i, 5*i))
	sys.stdout.flush()
	return

# read data
data = json.loads(open('data.json').read())
# print data['data'][0]

# create base folder
baseDirName = data['folder']
if not os.path.exists(baseDirName):
	os.makedirs(baseDirName)
	trace('folder created', baseDirName)

for catagory in data['catagories']:
	catDirName = baseDirName+'/'+catagory['folder']
	if not os.path.exists(catDirName):
		os.makedirs(catDirName)
		trace('folder created', catDirName)

	for subcategory in catagory['subcategories']:
		subCatDirName = baseDirName+'/'+catagory['folder']+'/'+subcategory['link']
		if not os.path.exists(subCatDirName):
			os.makedirs(subCatDirName)
			trace('folder created', subCatDirName)

		trace('loading', catagory['folder']+'/'+subcategory['link'])
		problemsURL = data['restbaseurl']+'/categories/'+catagory['folder']+'|'+subcategory['link']+"/challenges?"
		offset=0
		limit=10
		problemJSON = json.load(urllib2.urlopen(problemsURL+"offset="+str(offset)+"&limit="+str(limit)))
		total = problemJSON['total'] 
		received = limit
		# trace("show", received, False)
		while total > received:
			offset = received
			page = json.load(urllib2.urlopen(problemsURL+"offset="+str(offset)+"&limit="+str(limit)))
			received = received + limit
			# trace("show",page)
			for model in page['models']:
				problemJSON['models'].append(model)
			# trace('count',len(problemJSON['models']))
		
		# save json
		probsFileName = subCatDirName+'/' + 'problems.json'
		with open(probsFileName, 'a') as outfile:
			json.dump(problemJSON, outfile, indent=4)
			trace("file create", probsFileName)

		# create problems folder
		problemFoldername = subCatDirName+"/problems"
		if not os.path.exists(problemFoldername):
			os.makedirs(problemFoldername)
			trace('folder created', problemFoldername)

		# load problems
		# https://www.hackerrank.com/rest/contests/master/challenges/solve-me-first
		current = 1 
		total = len(problemJSON['models'])
		for problem in problemJSON['models']:
			problemdataURL = data['restbaseurl']+'/challenges/'+problem['slug']
			progressbar(current, total)
			problemDataJSON = json.load(urllib2.urlopen(problemdataURL))

			# save problem json
			probFileName = problemFoldername + '/'+ problem['slug'] + '.json'
			with open(probFileName, 'a') as outfile:
				json.dump(problemDataJSON, outfile, indent=4)
				current +=1
				# trace("file create", probFileName)

		# break
	# break
