import requests
import sys
import csv
from bs4 import BeautifulSoup, SoupStrainer
import xml.etree.ElementTree as ET

#get input ticker or CIK from user
k = input('ticker or CIK: ')

if k.isdigit() == 1:
    print('CIK')
    #url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=' + str(k) + '&owner=exclude&action=getcompany'
else:
    print('ticker')
    #url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK='+str(k)+'&owner=exclude&action=getcompany&Find=Search'


#GENERALIZE MORE BY PUTTING IN TYPE OF F13 AS SOMETHING THAT CAN BE CHANGED
#get link to
url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='+str(k)+'&type=13F&dateb=&owner=exclude&count=40'
print(url)

#access webpage source code
source_code = requests.get(url)
plain_text = source_code.text
soup = BeautifulSoup(plain_text, 'html.parser')

link = soup.findAll('a', id= 'documentsbutton')[0]
href = link.get('href')
link = 'https://www.sec.gov'+str(href) #gets us to page where we have the files desired
print(link)

#last part to access the actual forms
s2 = requests.get(link)
p2 = s2.text
sp2 = BeautifulSoup(p2, 'html.parser')
table = sp2.find_all('td', string= 'INFORMATION TABLE')
#print('table: ', table[1].previous_sibling.previous_sibling)
a = table[1].previous_sibling.previous_sibling
for child in a.children:
    end = child['href']

xml = "https://www.sec.gov" + end
xmlStuff = requests.get(xml)
xml2 = xmlStuff.text
print(xml2)
##################################################

tree = ET.parse(xmlStuff.read())
root = tree.getroot()

filename = k + "_13F_" + ".txt"
saveFile = open(filename, 'w')

# Field names
fieldnames = []
for element in root[0]:
    fieldnames.append(element.tag.replace("{http://www.sec.gov/edgar/document/thirteenf/informationtable}", ""))
    for child in element:
        # Some elements have sub-elements
        fieldnames.append(child.tag.replace("{http://www.sec.gov/edgar/document/thirteenf/informationtable}", ""))


# Open tab-delimited CSV writing and write table headings

print('DONE')





