import requests
from bs4 import BeautifulSoup
import sys
import time

def getUrl():
	head = {
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
	}
	request = requests.get('http://musicforprogramming.net/',headers = head)
	soup = BeautifulSoup(request.content,'html.parser')
	content = soup.select('div[id="episodes"] a')
	urlFront = 'http://datashat.net/music_for_programming_'
	musicLinks = {}
	for i in content:
		musicName = (i.text).replace(': ','-').replace(' ','_').lower()
		if 	musicName.startswith("0"):
			musicName = musicName[1:]
		musicLinks[musicName] = '{0}{1}.mp3'.format(urlFront,musicName)
	new = {}
	new.update(list(musicLinks.items())[0:5])
	
	return new

def downloadMP3(link):
	fileName , url = link
	r = requests.get(url, stream=True)
	with open('{0}.mp3'.format(fileName), 'wb') as f:

		for chunk in r.iter_content(chunk_size=4096): 
			if chunk:
				f.write(chunk)
		f.close()
		return fileName

def forloopDownload():
	urls = getUrl()
	complete = 0
	completeInTerminal(complete,len(urls))
	for item in urls.items():
		downloadMP3(item)
		complete += 1
		completeInTerminal(complete,len(urls))

import gevent
from gevent import monkey
def geventDownload():
	urls = getUrl()
	monkey.patch_all()

	jobs = [gevent.spawn(downloadMP3, item) for item in urls.items()]

	complete = 0
	completeInTerminal(complete,len(urls))
	for job in jobs:
		job.join()
		complete += 1
		completeInTerminal(complete,len(urls))

def completeInTerminal(complete,total):
	done = int(30 * complete / total)
	sys.stdout.write("\r已完成(%s/%s)[%s%s]" % (complete, total, '#'*done, '-'*(30 - done)))
	sys.stdout.flush()

timeStart = time.time()
geventDownload()
#forloopDownload()
timeEnd = time.time()
print("\r\n共費時 : %s 秒" % (timeEnd-timeStart))
