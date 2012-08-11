from BeautifulSoup import BeautifulSoup
import urllib2
import datetime

class MSL_Images():
  """Class to get images from NASA's MSL raw data pages. Call get_images() for json output"""

  # setup
  baseurl  = "http://mars.jpl.nasa.gov/msl/multimedia/raw/"
  
  def __init__(self, vebose=False):
    self.verbose = vebose
  
  def get_images(self):
    sols = []
    data = {}
    for sol in range(10):
      print "getting sol %d" % sol
      
      sol_data = self.get_images_from_sol(sol)
      if not sol_data:
        print "404, finished at sol %d" % (sol - 1)
        break
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
        print "404, no sol data"
      return None

    if self.verbose:
      print "opening", url

    # Objects to dump into json later
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
          
          # URL
          # Get the image url and remove thumbnail
          image = cell.find('img')
          src   = image['src']
          # test for thumbnail
          if "-thm.jpg" in src:
            src = src[0:-8] + ".JPG"
          if self.verbose:
            print src,
          
          # caption
          caption = cell.find('div', { "class" : "RawImageCaption" })
          thumbnail = True
          # this is where it says "thumbnail" or "full"
          if "full" in caption.contents[2]:
            thumbnail = False    
          if self.verbose:
            print caption.contents[2],
          
          # image date time
          date = cell.find('div', { "class" : "RawImageUTC" })
          dt_string = date.string[0:-9]
          dt   = datetime.datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
          if self.verbose:
            print dt
          
          images.append({"rawid": raw_id, "thumb": thumbnail, "uri": src, "datetime": dt.isoformat()})
          
    if len(images) > 0:
      instruments.append({"instrument_name": instrument_name, "images": images})

    return instruments
