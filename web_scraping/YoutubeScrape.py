# -*- coding: utf-8 -*-
"""
Created on Tuesday 18/02/2020 11:37

@author: Laura
"""

from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import sys
from time import sleep

def update_progress_bar(current_count, total_count):
	
	current_percent = ((current_count + 1) / total_count)
	bar_hash = '#'*(int(current_percent * 30))
	bar_space = ' '*(30-len(bar_hash))
	
	sys.stdout.write('\r')
	sys.stdout.write(f'[{bar_hash}{bar_space}] {int(current_percent * 100)}% {current_count + 1}/{total_count}')
	sys.stdout.flush()


# Create Data Frames to store results
plColNames = ['Day', 'DayTitle', 'DayURL', 'NumVids']
playlistOutput = pd.DataFrame(columns = plColNames)
vColNames = ['Day', 'VideoTitle', 'VideoURL', 'AddedBy', 'Likes', 'Dislikes', 'views']
videosOutput = pd.DataFrame(columns = vColNames)

# import playlist info
playlistsInput = pd.read_csv('ListOfPlaylists.csv')

for playlist in playlistsInput.index:
	
	
	# Get playlistInfo from ListOfPlaylists.csv
	playlistDay = playlistsInput['Day'][playlist]
	playlistTitle = playlistsInput['Title'][playlist]
	playlistURL = playlistsInput['Link'][playlist]
	
	# Get page html from link from ListOfPlaylists.csv and parse
	playlistPage = requests.get(playlistsInput['Link'][playlist])
	page = playlistPage.text
	soup=bs(page,'html.parser')
	
	# Scrape all links to individual videos and store as array
	videoLinks=soup.find_all('tr', {'class':'pl-video yt-uix-tile'})
	playlistLen = len(videoLinks) # ToDo: Change this to something that checks if video links are found and reloads if not?? check staff names and video links are same length
	
	playlistOutput.loc[len(playlistOutput)] = [playlistDay, playlistTitle, playlistURL, playlistLen]
	

playlistOutput.to_csv('playlists_details.csv', encoding='utf-8', index=False)

			
		

		
		
		
		
		
		
		

#	
#	r = requests.get(playlistsInput['Link'][playlist])
#	page = r.text
#	soup=bs(page,'html.parser')
#	#print(soup.prettify())
#	with open("output1.html", "w", encoding='utf-8') as file:
#		file.write(str(soup))
#	links=soup.find_all('a',{'class':'pl-video-title-link'})
#	print(playlistsInput['Title'][playlist])
#	playlistLen = len(links)
#	print(str(playlistLen))
#	for l in links:
#		print(l.get("href"))





#	if (playlistLen == 0):
#		with open("output2.html", "w", encoding='utf-8') as file:
#			file.write(str(soup))


	
	
	
	
#	# This will get the div
#div_container = soup.find('div', class_='some_class')  
#
## Then search in that div_container for all p tags with class "hello"
#for ptag in div_container.find_all('p', class_='hello'):
#    # prints the p tag content
#    print(ptag.text)