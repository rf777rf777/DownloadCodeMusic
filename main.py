import requests
from bs4 import BeautifulSoup
import sys
import time
import os

def chooseSong():
	allSong = getUrl()
	print('\n======================== Song List ========================\n\nDownload songs from "http://musicforprogramming.net/"\n\n===========================================================\n')
	for name in allSong.keys():
		index = list(allSong.keys()).index(name)
		#print(list(allSongName).index(i) % 5)
		if (index+1) % 3 == 0 :
			print(name)
		else:
			print('{0: <30}'.format(name), end=' ')
	
	songLink = []
	while True:
		choice = input("\n\nPlease enter song numbers ( ex : 1 , 10 , 25) or 'All' to download：")
		try:
			if choice == "All":
				songLink = list(allSong.items())
			else:
				choice = choice.split(',')
				for i in choice:
					songLink.append(list(allSong.items())[int(i)-1])
			break
		except Exception as e:
			print("\nError,Please try again. ( ex : 1 , 10 , 25 )")
			pass

	return songLink

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

	return musicLinks

def downloadMP3(link):
	folder = folderDefine()
	fileName , url = link
	r = requests.get(url, stream=True)
	with open('{0}/{1}.mp3'.format(folder, fileName), 'wb') as f:
		for chunk in r.iter_content(chunk_size=512): 
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
	urls = chooseSong()
	monkey.patch_all()

	jobs = [gevent.spawn(downloadMP3, item) for item in urls]
	print("Downloading...\n")
	complete = 0
	completeInTerminal(complete,len(urls))
	for job in jobs:
		job.join()
		complete += 1
		completeInTerminal(complete,len(urls))

def completeInTerminal(complete,total):
	done = int(30 * complete / total)
	sys.stdout.write("\rCompleted：( %s / %s )[ %s%s ]" % (complete, total, '#'*done, '-'*(30 - done)))
	sys.stdout.flush()

def folderDefine():
	#if執行exe檔
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        #print('系統名稱:'+os.name)
        if os.name == 'nt':
            symbol = "\\"
        else :
            symbol = "/"
        musicFloder_path = application_path.rpartition(symbol)[0]+'/{0}'.format("CodingMusic")
    #if直接執行.py檔
    elif __file__:
        musicFloder_path = "CodingMusic" 
    return musicFloder_path

timeStart = time.time()
geventDownload()
#forloopDownload()
timeEnd = time.time()
print("\r\nTotal Time : %s seconds" % (timeEnd-timeStart))

if os.name == 'nt':
	input("\n<<< Press Enter >>>")