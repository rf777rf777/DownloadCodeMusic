# DownloadCodeMusic - CodeMusic音樂下載器
![image](https://upload.cc/i1/2018/04/16/Rx30tI.jpg)
## :pencil2: 概述

將 **[MusicForProgramming](http://musicforprogramming.net/)** 網站中的音樂下載到本地的 Terminal / Console 程式。

## :closed_book: 特色
  + 使用 [Requests](http://docs.python-requests.org/en/master/)、[BeautifulSoup](http://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/)， 進行 **歌曲名稱** 以及 **歌曲串流(Stream)** 的 HTTP 請求與解析。
  + 使用 [Gevent](http://www.gevent.org/)，下載多首歌曲。
  + 本範例可在 Windows / macOS 環境下執行。

## :green_book: 安裝專案
1. 本程式執行的最佳環境為：[Python3.6](https://www.python.org/downloads/)，請確認自己電腦或虛擬環境內的 Python 版本。

2. Clone / Download 這個專案：
    
        git clone https://github.com/rf777rf777/DownloadCodeMusic.git
3. 在 Terminal / Console(cmd) 輸入：
  
        pip install -r requirements.txt
    
   來安裝需要的 Packages。

## :blue_book: 使用方法
1. 在 Terminal / Console (cmd) 輸入：

        python main.py

2. 輸入要下載的歌曲號碼後按下 Enter 鍵，不同號碼間請用 **"，"** 分隔，或輸入 **"All"** 來下載全部歌曲。

	![image](https://upload.cc/i1/2018/04/16/B80WAl.jpg)

3. 下載完成後會產生一個 :file_folder: **CodingMusic** ，存放剛剛下載的歌曲。

	![image](https://upload.cc/i1/2018/04/16/OWZYAC.jpg)

## :books: Library or API Reference

[Requests - ver2.18.4](https://pypi.python.org/pypi/requests).

[BeautifulSoup - ver4.6.0](https://pypi.python.org/pypi/beautifulsoup4).

[Gevent - ver1.2.2](https://pypi.python.org/pypi/gevent).

## :memo: License
[MIT](https://zh.wikipedia.org/wiki/MIT%E8%A8%B1%E5%8F%AF%E8%AD%89)