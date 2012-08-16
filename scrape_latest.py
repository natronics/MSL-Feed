#!/usr/bin/env python
import nasa
import json
import redis
import datetime
import time
import config

r = redis.StrictRedis(host=config.redis_host, port=config.redis_port, db=config.redis_db)

def sanitize_name(name):
  name = name.translate(None, ' ()!@#$%^&*{}[]|\/<>,.;:~`+=_-')
  return name

def add_image(sol, instrument, isThumb, storeobj):
  now = datetime.datetime.now()
  now = int(time.mktime(now.timetuple()))
  
  # All Feed
  r.zadd('msl-all-feed', now, storeobj)
  r.sadd('msl-feeds', 'msl-all-feed')
  r.set('msl-all-feed-name', 'Latest Images from MSL')
  
  # Instrument
  feed_name = 'msl-%s-feed' % sanitize_name(str(instrument))
  r.zadd(feed_name, now, storeobj)
  r.sadd('msl-feeds', feed_name)
  r.set(feed_name + '-name', 'Latest Images from %s on MSL' % str(instrument).split('(')[0].strip())
  
  if not isThumb:
    # All Feed No Thumbs
    r.zadd('msl-all-feed-nothumb', now, storeobj)
    r.sadd('msl-feeds', 'msl-all-feed-nothumb')
    r.set('msl-all-feed-nothumb-name', 'Latest Images from MSL - Full Resolution Images Only')
    
    # Instrument
    feed_name = 'msl-%s-feed-nothumb' % sanitize_name(str(instrument))
    r.zadd(feed_name, now, storeobj)
    r.sadd('msl-feeds', feed_name)
    r.set(feed_name + '-name', 'Latest Images from %s on MSL - Full Resolution Images Only' % str(instrument).split('(')[0].strip())


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
      #uri      = image['uri']
      
      # Test if we've seen this image before
      # if not, add it to redis database of images and feeds
      if not r.sismember('msl-images', image_id):
        
        uri = scraper.get_image_uri(image_id)
        obj = json.dumps({"rawid": image_id, "nasatime": nasatime, "instrument": inst_name, "uri": uri})
        print "new image!!!",
        print sol_num, inst_name, uri
        
        # let us know if we've seen it before
        r.sadd('msl-images', image_id)
        
        # Adds metadata to all the feeds
        add_image(sol_num, inst_name, thumb, obj)

