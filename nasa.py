#!/usr/bin/env python
from BeautifulSoup import BeautifulSoup
import urllib2
import datetime
import json

# Scraping setup
url  = "http://mars.jpl.nasa.gov/msl/multimedia/raw/"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)

# Objects to dump into json later
data        = {}
sols        = []
instruments = []
images      = []

# Table based layout!
# Grab the table cell with the main content
content     =  soup.find('td', { "class" : "pageContent" })

# The second table is the list of images
image_table =  content.findAll('table')[1]

for row in image_table.findAll('tr'):
  cells = row.findAll('td')
  header = row.findAll('td', { "class" : "CameraName" })
  
  # See if we're in a header
  if len(header) > 0:
    instrument_name = header[0].string
    #print instrument_name
    
    # there is data from the last instrument to push!
    if len(images) > 0:
      instruments.append({"name": instrument_name, "images": images})
      images = []
      
  else:
    #Not in a header, we expect images:
    for cell in cells:
      # the link has the raw id
      link = cell.find('a')
      raw_id = link['href'][9:-4]  # scrape away the query string crap
      #print raw_id,
      
      # caption
      caption = cell.find('div', { "class" : "RawImageCaption" })
      thumbnail = True
      # this is where it says "thumbnail" or "full"
      if "full" in caption.contents[2]:
        thumbnail = False    
      #print caption.contents[2],
      
      # image date time
      date = cell.find('div', { "class" : "RawImageUTC" })
      dt_string = date.string[0:-9]
      dt   = datetime.datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
      #print dt
      
      images.append({"rawid": raw_id, "thumb": thumbnail, "datetime": dt.isoformat()})
      
if len(images) > 0:
  instruments.append({"name": instrument_name, "images": images})

print json.dumps(instruments)
