import urllib2, json, pprint, re, datetime, json

# list of pages to be parsed (using friendly name)
pageNames = ["4 Vesta", "Ceres (dwarf planet)", "433 Eros", 
  "25143 Itokawa", "(285263) 1998 QE2", "(136617) 1994 CC", 
  "(153591) 2001 SN263"]

pages = [
  "https://en.wikipedia.org/wiki/4_Vesta",
  "https://en.wikipedia.org/wiki/Ceres_(dwarf_planet)",
  "https://en.wikipedia.org/wiki/433_Eros",
  "https://en.wikipedia.org/wiki/25143_Itokawa",
  "https://en.wikipedia.org/wiki/(285263)_1998_QE2",
  "https://en.wikipedia.org/wiki/(136617)_1994_CC",
  "https://en.wikipedia.org/wiki/(153591)_2001_SN263"
]

# list of infobox keys we don't care about
excluded = ["image", "pronounced", "caption", "bgcolour", 
  "background", "surface_area", "discoverer", "<ref name"]

from bs4 import BeautifulSoup
import urllib2

def decode(str):
  return str.encode('utf-8').strip()

# initialize storage for parsed values
data = {}

for site in pages:
  req = urllib2.Request(site,headers={'User-Agent': 'Mozilla/5.0'})
  page = urllib2.urlopen(req)
  soup = BeautifulSoup(page.read(), "html.parser")
  table = soup.find('table', class_='infobox')
  result = {}

for tr in table.find_all('tr'):
  if tr.find('th') and tr.find('td'):
    key = decode(tr.find('th').text)
    value = decode(tr.find('td').text)
    result[key] = value
   
  name = site.replace('https://en.wikipedia.org/wiki/', '') 
  data[name] = result

# csv
csv = ""

# generate a superset of possible values
keys = []
for entry in data:
  keys += data[entry].keys()
  keys = set(filter(None, keys)) # reduce to non empty set' ADDED TAB

# header row
header = "Target\t"
for key in keys:
  header += key + "\t"
csv += header + "\n" #INVALID SYNTAX ERROR?

# rows
for entry in data:
  row = entry + "\t" # target col
  for key in keys:
  	if key in data[entry]:
  	  row += data[entry][key] + "\t"
  	else:
  	  row += "NULL\t"
  csv += row + "\n"

with open("output.csv", "w") as text_file:
    text_file.write(csv)

print "Completed.  Results at output.csv."
