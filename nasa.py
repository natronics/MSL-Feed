from BeautifulSoup import BeautifulSoup
import urllib2
import datetime
import time
import math


MSL_KEY = {"NLA":
    { 
      "name":       "Navcam: Left A", 
      "ext":        ".JPG", 
      "url_prefix": "http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/%05d/opgs/edr/ncam/"
    }
  , "NRA": 
    { 
      "name": "Navcam: Right A", 
      "ext": ".JPG", 
      "url_prefix": "http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/%05d/opgs/edr/ncam/"
    }
  , "CR0":
    { 
      "name": "ChemCam: Remote Micro-Imager ", 
      "ext": ".JPG", 
      "url_prefix": "http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/%05d/opgs/edr/ccam/"
    }
  , "MR":
    { 
      "name": "MastCam Right", 
      "ext": ".jpg", 
      "url_prefix": "http://mars.jpl.nasa.gov/msl-raw-images/msss/%05d/mcam/"
    }
  , "ML":
    {
      "name": "MastCam Left", 
      "ext": ".jpg", 
      "url_prefix": "http://mars.jpl.nasa.gov/msl-raw-images/msss/%05d/mcam/"
    }
  , "MH": 
    {
      "name": "Mars Hand Lens Imager (MAHLI)", 
      "ext": ".jpg", 
      "url_prefix": "http://mars.jpl.nasa.gov/msl-raw-images/msss/%05d/mhli/"
    }
  , "MD":
    {
      "name": "Mars Descent Imager (MARDI)", 
      "ext": ".jpg",
      "url_prefix": "http://mars.jpl.nasa.gov/msl-raw-images/msss/%05d/mrdi/"
    }
  , "FLA": 
    {
      "name": "Front Hazcam: Left A", 
      "ext": ".JPG",
      "url_prefix": "http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/%05d/opgs/edr/fcam/"
    }
  , "FRA": 
    { 
      "name": "Front Hazcam: Right A", 
      "ext": ".JPG",
      "url_prefix": "http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/%05d/opgs/edr/fcam/"
    }
  , "RRA":
    {
      "name": "Rear Hazcam: Right A", 
      "ext": ".JPG",
      "url_prefix": "http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/%05d/opgs/edr/rcam/"
    }
  , "RLA":
    {
      "name": "Rear Hazcam: Left A", 
      "ext": ".JPG",
      "url_prefix": "http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/%05d/opgs/edr/rcam/"
    }}

class MSL_Images():
  """Class to get images from NASA's MSL raw data pages. Call get_images() for json output"""

  # setup
  baseurl  = "http://mars.jpl.nasa.gov/msl/multimedia/raw/"
  
  def __init__(self, vebose=False):
    self.verbose = vebose
  
  def tosol(self):
    now = datetime.datetime.now()
    
    # Calculate MSD
    # MSD = (seconds since January 6, 2000 00:00:00 UTC)/88775.244 + 44795.9998 
    # Mars epoch in local time (+8)
    epoch = datetime.datetime(2000,1,6,8,0,0)
    s     = ((now - epoch).days*86400) + (now - epoch).seconds
    MSD   = (s/88775.244) + 44795.9998
    
    # Calculate number of Sols since MSL landing
    # Landing Time: 49269 05:50:16
    sol = MSD - 49269.2432411704
    sol = sol + 1  # for sol 0
    sol = int(math.ceil(sol))
    
    return sol
  
  def get_images(self):
    """Gets all images from the last two weeks of sols on Mars"""
    data = {}
    
    # Get current Sol
    sol = self.tosol()
    
    # Go back one Mars fortnight through tosol
    for sol in range(sol-14, sol+1):
      print "getting sol %d" % sol
      # get on sol of images
      sol_data = self.get_images_from_sol(sol)
      if not sol_data:
        print "sol %d not retrieved" % sol
      else:
        now = datetime.datetime.now()
        now = int(time.mktime(now.timetuple()))
        data["%d"%sol] = {"images": sol_data, "time": now}
      time.sleep(1)
      
          
    return data
  
  def get_images_from_sol(self, sol):
    """Scrapes JPL's site for all images in a given sol"""
    
    # webpage for given sol
    url  = self.baseurl + '?s=%d' % sol
    
    if self.verbose:
      print "opening", url
    
    # ignore any network errors with try: catch
    try:
      page = urllib2.urlopen(url)
      soup = BeautifulSoup(page)
    except:
      if self.verbose:
        print "sol url failed to open"
      return None
    
    # Objects to dump into json later
    images      = []
    
    # Table based layout!
    # The fifth table is the list of images
    # there are no semantics to help here :/
    cells =  soup.findAll('table')[5].findAll('td')

    for cell in cells:
      link = cell.find('a')
      if link:
        image = link.find('img')
        if image:
          # MSL images are inside an anchor inside a table cell. So we assume
          # this is a mars image. We get the image url and scrape the image id
          # from it
          thumbnail_url = image['src']
          image_id      = thumbnail_url.split('/')[-1][0:-8] 
          images.append(image_id)

    return images

  def get_image_uri(self, rawid):
    """depreciated"""
    
    url  = self.baseurl + '?rawid=%s' % rawid
    try:
      page = urllib2.urlopen(url)
      soup = BeautifulSoup(page)
    except:
      if self.verbose:
        print "404, image not found"
      return None

    if self.verbose:
      print "opening", url
    
    uri_link =  soup('a',text='Full Resolution')[0].parent
    return uri_link["href"]
    
