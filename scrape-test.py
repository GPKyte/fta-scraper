import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

def scrape_sale(sale):
    link = "https://bid.bidfta.com/cgi-bin/mnprint.cgi?{}".format(sale)
    page = urllib2.urlopen(link)
    soup = BeautifulSoup(page, 'lxml')

    catalog = soup.find('table', { 'id': 'DataTable' })

    conn = sqlite3.connect("fta.sqlite")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS items (\
        location text, \
        id text, \
        description text, \
        info text, \
        UNIQUE(id) ON CONFLICT REPLACE)")

    args = []
    for row in catalog.findAll("tr")[1:]:
        cells = row.findAll('td')
        itemId = cells[0].find(text=True).strip(".")
        description = None
        info = None
        location = None

        #itemLink = "https://bid.bidfta.com/cgi-bin/mnlist.cgi?{}/{}" \
        #    .format(sale, itemCode)


        print(itemId)
        details = cells[1].findAll('b')
        for elem in details:
            tag = elem.find(text=True)
            content = elem.next_sibling
            if (not content):
                continue
            if (content[0] == ":"):
                content = content[2:]
            print("    {}: {}".format(tag, content))

            if (tag == "Item Description"):
                description = content
            elif (tag == "Additional Info"):
                info = content
            elif (tag == "Item Location"):
                location = content
            else:
                pass

            if (description and info and location):
                break

        args.append((
            location,
            itemId,
            description,
            info))

    cursor.executemany(
        "INSERT INTO items(location, id, description, info) \
        VALUES(?,?,?,?)", args)
    conn.commit()


sale = "schoolii1969"
scrape_sale(sale)
