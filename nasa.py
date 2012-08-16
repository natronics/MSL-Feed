from BeautifulSoup import BeautifulSoup
import urllib2
import datetime
import math

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
    sols = []
    data = {}
    
    # Get current Sol
    sol = self.tosol()
    
    # Go back one Mars fortnight
    for sol in range(sol-14, sol+1):
      if sol >=0:
        print "getting sol %d" % sol
        
        sol_data = self.get_images_from_sol(sol)
        if not sol_data:
          print "sol %d 404" % sol
        else:
          sols.append(sol_data)
    
    data["sols"] = sols
    return data
  
  def get_images_from_sol(self, sol):
 
    # get page for sol
    url  = self.baseurl + '?s=%d' % sol
    try:
      page = urllib2.urlopen(url)
      soup = BeautifulSoup(page)
    except:
      if self.verbose:
        print "sol lookup failed"
      return None

    if self.verbose:
      print "opening", url

    # Objects to dump into json later
    instruments = []
    images      = []
    
    # Table based layout!
    # The fifth table is the list of images
    # there are no semantics to help here
    image_table =  soup.findAll('table')[5]

    for row in image_table.findAll('tr'):
      cells = row.findAll('td')
      header = row.findAll('td', { "class" : "CameraName" })
      
      # See if we're in a header
      if len(header) > 0:
        instrument_name = header[0].string
        if self.verbose:
          print instrument_name
        
        # there is data from the last instrument to push!
        if len(images) > 0:
          instruments.append({"instrument_name": instrument_name, "images": images})
          images = []
          
      else:
        #Not in a header, we expect images:
        for cell in cells:
          # the link has the raw id
          link = cell.find('a')
          raw_id = link['href'][9:-4]  # scrape away the query string crap
          if self.verbose:
            print raw_id,
          
          # caption, this is where it says "thumbnail" or "full"
          caption = cell.find('div', { "class" : "RawImageCaption" })
          caption = "".join([str(x) for x in caption.contents]) 
          thumbnail = True
          if "full" in caption or "subframe" in caption:
            thumbnail = False    
          if self.verbose:
            print caption, thumbnail
          
          # image date time
          date = cell.find('div', { "class" : "RawImageUTC" })
          dt_string = date.string[0:-9]
          dt   = datetime.datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
          if self.verbose:
            print dt
          
          images.append({"rawid": raw_id, "thumb": thumbnail, "datetime": dt.isoformat()})
          
    if len(images) > 0:
      instruments.append({"instrument_name": instrument_name, "images": images})

    return instruments

  def get_image_uri(self, rawid):
  
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
    
