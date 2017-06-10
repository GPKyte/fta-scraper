import urllib2
import sqlite3
import string

from bs4 import BeautifulSoup
from byteify import byteify

def scrape_sale(sale):
    page = urllib2.urlopen(sale)
    soup = BeautifulSoup(page, 'lxml')

    catalog = soup.find('table', { 'id': 'DataTable' })

    conn = sqlite3.connect("fta.sqlite")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS items (\
        location text, \
        timeout text, \
        sale text, \
        itemId text, \
        link text, \
        info text, \
        description text, \
        UNIQUE(itemId) ON CONFLICT REPLACE)")
    
    timeout = "June 10, 2017 2:15 PM EST"
    header = soup.find('div', id='wrapper').find('p', align='center')
    title = header.findAll(text=True)[1]
    timeout = byteify(title.split(' - ')[-1])

    args = []
    for row in catalog.findAll("tr")[1:]:
        cells = row.findAll('td')
        itemId = cells[0].find(text=True).strip(".")
        description = None
        info = None
        location = None

        itemPage = string.replace(sale, "mnprint", "mnlist")
        link = "{}/{}".format(itemPage, itemId)


        details = cells[1].findAll('b')
        for elem in details:
            tag = elem.find(text=True)
            content = elem.next_sibling.strip()
            if (not content):
                continue
            if (content[0] == ":"):
                content = content[2:]

            if ("Description" in tag):
                description = content
            elif ("Additional Info" in tag):
                info = content
            elif ("Item Location" in tag):
                location = content
            else:
                pass

            if (description and info and location):
                break

        args.append((
            location,
            timeout,
            sale,
            itemId,
            link,
            info,
            description))

    cursor.executemany(
        "INSERT INTO items(location, timeout, sale, itemId, \
                link, info, description) \
        VALUES(?,?,?,?,?,?,?)", args)
    conn.commit()
