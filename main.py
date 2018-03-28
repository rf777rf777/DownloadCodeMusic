import requests
from bs4 import BeautifulSoup
import sys
import time
import os
import gevent
from gevent import monkey

#Choose songs you want
def chooseSong():
	allSong = getUrl()
	print('\n{0} Song List {0}\n\nDownload songs from "http://musicforprogramming.net/"\n\n{1}\n'.format('='*24,'='*59))
	for name in allSong.keys():
		index = list(allSong.keys()).index(name)
		#print(list(allSongName).index(i) % 5)
		if (index+1) % 3 == 0 :
			print(name)
		else:
			print('{0: <30}'.format(name), end=' ')
	
	while True:
		songLink = []
		choice = input("\n\nPlease enter Music numbers ( ex : 1 , 10 , 25) or 'All' to download：")
		try:
			if choice == "All":
				songLink = list(allSong.items())
			else:
				choice = choice.split(',')
				for i in choice:
					index = int(i)
					if index in range(1,len(allSong)+1) :
					    songLink.append(list(allSong.items())[index-1])
					else :
						print('Invalid Music number : "{0}"'.format(i))
			if songLink:
				break
		except Exception as e:
			print("\nError,Please try again. ( ex : 1 , 10 , 25 )")
			pass

	return songLink

#Get songs downloadLinks from website(http://musicforprogramming.net/)
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

#Download mp3 of the link
def downloadMP3(link):
	folder = folderDefine("CodingMusic",True)
	fileName , url = link
	r = requests.get(url, stream=True)
	with open('{0}/{1}.mp3'.format(folder, fileName), 'wb') as f:
		for chunk in r.iter_content(chunk_size=512): 
			if chunk:
				f.write(chunk)
		f.close()
		return fileName

#Use "for loop" to download one by one 
def forloopDownload():
	urls = getUrl()
	complete = 0
	completeInTerminal(complete,len(urls))
	for item in urls.items():
		downloadMP3(item)
		complete += 1
		completeInTerminal(complete,len(urls))

#Use gevent to download
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

#ProgressBar on Terminal  
def completeInTerminal(complete,total):
	done = int(30 * complete / total)
	sys.stdout.write("\rCompleted：( %s / %s )[ %s%s ]" % (complete, total, '#'*done, '-'*(30 - done)))
	sys.stdout.flush()

#Find the folder location
def folderDefine(folderName,pyinstallerClean):
	#if執行exe檔
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)

		#If exe file was created by "pyinstaller XXX.py -F"        
        if pyinstallerClean:
        	musicFloder_path = application_path + '/{0}'.format(folderName)
       	# created by "pyinstaller XXX.py" (without "-F" tag)
       	else:
            if os.name == 'nt':
                symbol = "\\"
            else :
                symbol = "/"
            musicFloder_path = application_path.rpartition(symbol)[0]+'/{0}'.format(folderName)
    #if直接執行.py檔
    elif __file__:
        musicFloder_path = folderName 
    if not os.path.exists(musicFloder_path):
        os.makedirs(musicFloder_path)

    return musicFloder_path

def main():
	timeStart = time.time()
	geventDownload()
	#forloopDownload()
	timeEnd = time.time()
	print("\r\nTotal Time : {0} seconds".format(timeEnd-timeStart))

if __name__ == '__main__':
    main()

if os.name == 'nt':
	input("\n<<< Press Enter >>>")