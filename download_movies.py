import urllib2
import os
import wget
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

link ="http://dayt.se/forum"

#url=urllib.urlopen(link)
def initialize_opener():
	"""
	Initializes the opener object adds header content and returns it 
	"""
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Opera/9.25')]
	return opener

#url = opener.open(link+"/forum.php")
def read_content(link,opener):
	"""
	Reads the content for the given link and returns it :)

	"""
	request = urllib2.Request()
	content=opener.open(request).read()
	return content

#print content
opener=initialize_opener()
content=read_content(link+"/forum.php",opener)
soup=BeautifulSoup(content,'html.parser')

series_list=[]
for sec in soup.find_all('span',attrs={'class':'sectiontitle'}):
	episodes_link = link+'/'+sec.a.get('href')
	series_name=sec.a.string
	series_list.append([series_name,episodes_link])

cnt=1
for series in series_list:
	print str(cnt)+"."+series[0]
	cnt+=1

print "Enter the series No: to get the list of episodes to download"
seriesno=int(raw_input())
series=series_list[seriesno-1]
link_ep=series[1]

content=read_content(link_ep,opener)
#url = opener.open(link+"/forum.php")

episode_list=[]
soup=BeautifulSoup(content,'html.parser')
for sec in soup.find_all('a',attrs={'class':'title'}):
	episode_list.append([sec.string,link+'/'+sec.get('href')])
cnt=1	
for episode in episode_list:
	print str(cnt)+"."+episode[0]
	cnt+=1


print "Enter episode no: to download:"
episodeno=int(raw_input())
link_dwn=episode_list[episodeno-1][1]	

content=read_content(link_dwn,opener)
soup=BeautifulSoup(content,'html.parser')
down=soup.find('a',attrs={'id':'dm3'})
print down.get('href')
#filename = wget.download(down.get('href'))
profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2) # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', '/tmp')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')

browser = webdriver.Firefox(profile)
browser.get(down.get('href'))

#browser.find_element_by_id('exportpt').click()
#browser.find_element_by_id('exporthlgt').click()
