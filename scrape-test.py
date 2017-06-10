import urllib2
from bs4 import BeautifulSoup

sale = "schoolii1969"
link = "https://bid.bidfta.com/cgi-bin/mnprint.cgi?{}".format(sale)
page = urllib2.urlopen(link)
soup = BeautifulSoup(page, 'lxml')

catalog = soup.find('table', { 'id': 'DataTable' })

A=[] # Code
B=[] # Description
C=[] # Additional Info
D=[] # Location

for row in catalog.findAll("tr")[1:]:
    cells = row.findAll('td')
    itemCode = cells[0].find(text=True).strip(".")
    itemLink = "https://bid.bidfta.com/cgi-bin/mnlist.cgi?{}/{}" \
        .format(sale, itemCode)
    A.append(itemCode)
    print(itemCode)

    description = cells[1].findAll('b')
    for elem in description:
        tag = elem.find(text=True)
        content = elem.next_sibling
        if (not content):
            continue

        if (content[0] == ":"):
            content = content[2:]
        print("    {}: {}".format(tag, content))

        if (tag == "Item Description"):
            B.append(content)
        elif (tag == "Additional Info"):
            C.append(content)
        elif (tag == "Item Location"):
            D.append(content)
        else:
            pass

import pandas as pd
df=pd.DataFrame(A,columns=['Code'])
df['Description']=B
df['Additional Info']=C
df['Location']=D
print(df)
