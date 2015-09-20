import urllib2
from bs4 import BeautifulSoup
import mechanize;
from urllib2 import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time;
import eyed3;
import os;
print "How many songs do you want?";
count = input();
loop = 0;
while(loop < count):
	songPage = urllib2.urlopen("http://www.randomlists.com/random-songs")
	songSource = songPage.read()
	songPageContent = BeautifulSoup(songSource,"lxml");
	songPageContent.prettify()
	songAndArtistList = songPageContent.findAll('span',itemprop = True);
	songList = [];
	songList.append(str(songAndArtistList[1].string).split() + str(songAndArtistList[2].string).split());
	songList.append(str(songAndArtistList[4].string).split() + str(songAndArtistList[5].string).split());
	songList.append(str(songAndArtistList[7].string).split() + str(songAndArtistList[8].string).split());
	for eachSong in songList:
		YTURL = "http://www.youtube.com/results?search_query=" + "+".join(eachSong) + "+mp3";
		print "Yotube URL being searched is: " + YTURL;
		YTResponsePage = urllib2.urlopen(YTURL);
		YTResponse = YTResponsePage.read();
		YTResponseSource = BeautifulSoup(YTResponse,"lxml");
		YTResponseSource.prettify();
		YTSongList = YTResponseSource.findAll("div", { "class" : "yt-lockup-content" });
		if(len(YTSongList) == 0):
			print "Song Links not found. Continuing...";
			continue;
		YTSongLink = YTSongList[0].findAll("a");
		if(len(YTSongLink) == 0):
			print "No Links found. Continuing...";
			continue;
		if(YTSongLink[0].get('href') == None):
			print "None retrieved. Continuing...";
			continue;
		YTSong = "https://youtube.com" + str(YTSongLink[0].get('href'));
		if(YTSong == "__url__"):
			print "__url__ retrieved. Continuing...";
			continue;
		print "Link of song being downloaded: " + YTSong;
		#end of parsing code to get song URL. 
		
		#Begin of selenium tool to get JavaScript loaded URL value.
		driver = webdriver.Firefox()
		profile = webdriver.FirefoxProfile()
		profile.set_preference('browser.download.manager.showWhenStarting', False)
		driver.get("http://www.youtube-mp3.org/");
		time.sleep(3);
		driver.find_element_by_id("youtube-url").clear();
		MP3Form = driver.find_element_by_id("youtube-url");
		MP3Form.send_keys(YTSong);
		MP3Form.send_keys(Keys.RETURN);
		print "Waiting for page to load.";
		time.sleep(3);
		
		MP3DLLink = driver.find_element_by_id("dl_link");
		
		MP3DLURL = "";
		MP3Link = MP3DLLink.find_element_by_xpath("(//a)[1]");
		MP3URL = MP3Link.get_attribute('href');
		if(MP3URL.find("&ts_create=") != -1):
			MP3DLURL = MP3URL;
		
		MP3Link = MP3DLLink.find_element_by_xpath("(//a)[2]");
		MP3URL = MP3Link.get_attribute('href');
		if(MP3URL.find("&ts_create=") != -1):
			MP3DLURL = MP3URL;
		
		MP3Link = MP3DLLink.find_element_by_xpath("(//a)[3]");
		MP3URL = MP3Link.get_attribute('href');
		if(MP3URL.find("&ts_create=") != -1):
			MP3DLURL = MP3URL;
		
		MP3Link = MP3DLLink.find_element_by_xpath("(//a)[4]");
		MP3URL = MP3Link.get_attribute('href');
		if(MP3URL.find("&ts_create=") != -1):
			MP3DLURL = MP3URL;
		if(MP3DLURL == ""):
			print "Unable to find link for download. Continuing...";
			driver.close()
			continue;
			
		print "The file is being transferred from : " + MP3DLURL;
		
		#Downloading MP3URL using urllib2.
		f = urllib2.urlopen(MP3DLURL);
		data = f.read()
		songName = str(" ".join(eachSong)) + ".mp3";
		with open(("D:\Songs\Python Script\ " + songName), "wb") as code:
			code.write(data)
		driver.close()
		loop = loop+1;
		print "Downloaded ", loop ," song!";
time.sleep(20);