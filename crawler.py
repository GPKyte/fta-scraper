#
# This will take the main page and open
# the links on it
#
# Goal is to use this in conjunction
# with the scraping tool to scrape all
# relevant auction pages
#

import urllib2
from bs4 import BeautifulSoup
import datetime
import string

link='http://bidfta.com'
page=urllib2.urlopen(link)
soup=BeautifulSoup(page, 'lxml')
day=datetime.date.today().day
locations=("amazon","cleveland")

auctions=soup.findAll('div', { 'class' : 'medium-4 columns auction' })
for a in auctions:
    timeout=a.find('time').get('datetime')
    timeout=timeout[5:16]
    if int(timeout[3:5]) < day:
        continue

    location=a.find('p', class_="auctionLocation").find(text=True).lower()
    if not 'found' in ['found' if (loc in location) else '' for loc in locations]:
        continue

    link=a.find('a').get('href')
    link=string.replace(link, "mndetails", "mnprint")
    print("{} | {} | {}".format(timeout, location, link))

