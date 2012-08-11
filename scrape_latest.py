#!/usr/bin/env python
import nasa
import json
import redis
import datetime
import time

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def sanitize_name(name):
  name = name.translate(None, ' ()!@#$%^&*{}[]|\/<>,.;:~`+=_-')
  return name

def add_image(sol, instrument, isThumb, storeobj):
  now = datetime.datetime.now()
  now = int(time.mktime(now.timetuple()))
  
  # All Feed
  r.zadd('msl-all-feed', now, storeobj)
  r.sadd('msl-feeds', 'msl-all-feed')
  
  # Instrument
  feed_name = 'msl-%s-feed' % sanitize_name(str(instrument))
  r.zadd(feed_name, now, storeobj)
  r.sadd('msl-feeds', feed_name)
  
  # Sol
  feed_name = 'msl-sol%d-feed' % sol
  r.zadd(feed_name, now, storeobj)
  r.sadd('msl-feeds', feed_name)
  
  if not isThumb:
    # All Feed No Thumbs
    r.zadd('msl-all-feed-nothumb', now, storeobj)
    r.sadd('msl-feeds', 'msl-all-feed-nothumb')
    
    # Instrument
    feed_name = 'msl-%s-feed-nothumb' % sanitize_name(str(instrument))
    r.zadd(feed_name, now, storeobj)
    r.sadd('msl-feeds', feed_name)
    
    # Sol
    feed_name = 'msl-sol%d-feed-nothumb' % sol
    r.zadd(feed_name, now, storeobj)
    r.sadd('msl-feeds', feed_name)

#data =  json.loads(open('cache.json', 'r').read())

scraper = nasa.MSL_Images()
data    = scraper.get_images()

# Go through data
for sol_num, sol in enumerate(data['sols']):
  for instrument in sol:
    inst_name = instrument['instrument_name']
    for image in instrument['images']:
      image_id = image['rawid']
      nasatime = image["datetime"]
      thumb    = image['thumb']
      
      # Test if we've seen this image before
      # if not, add it to redis database of images and feeds
      if not r.sismember('msl-images', image_id):
        
        obj = json.dumps({"rawid": image_id, "nasatime": nasatime, "instrument": inst_name})
        print "new image!!!",
        print sol_num, inst_name, thumb, obj
        
        # let us know if we've seen it before
        r.sadd('msl-images', image_id)
        
        # Adds metadata to all the feeds
        add_image(sol_num, inst_name, thumb, obj)
        