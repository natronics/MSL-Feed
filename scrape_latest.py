#!/usr/bin/env python
import nasa
import json
import redis
import datetime
import time
import config

r = redis.StrictRedis(host=config.redis_host, port=config.redis_port, db=config.redis_db)

def add_image(sol, t, image):
 
  # All Feed
  r.zadd('msl-all-feed', t, json.dumps(image))
  r.sadd('msl-feeds', 'msl-all-feed')
  r.set('msl-all-feed-name', 'Latest Images from MSL')
  
  # instrument feed
  feedname = 'msl-%s-feed' % image['inst']
  r.zadd(feedname, t, json.dumps(image))
  r.sadd('msl-feeds', feedname)
  r.set('%s-name' % feedname, 'Latest Images from %s on MSL' % nasa.MSL_KEY[image['inst']]["name"])

  # No Thumbs:
  if image['t'] == False:
    # All Feed
    r.zadd('msl-all-feed-nothumb', t, json.dumps(image))
    r.sadd('msl-feeds', 'msl-all-feed-nothumb')
    r.set('msl-all-feed-nothumb-name', 'Latest Images from MSL - No Thumbnails')
   
    # instrument feed
    feedname = 'msl-%s-feed-nothumb' % image['inst']
    r.zadd(feedname, t, json.dumps(image))
    r.sadd('msl-feeds', feedname)
    r.set('%s-name' % feedname, 'Latest Images from %s on MSL - No Thumbnails' % nasa.MSL_KEY[image['inst']]["name"])
    
scraper = nasa.MSL_Images()
data    = scraper.get_images()

# Go through data
for sol in data:
  
  for image in data[sol]["images"]:
    # Test if we've seen this image before
    if not r.sismember('msl-images', image):
      print "new image!", image
      # image metadata conainter
      meta = {}

      solnum = int(sol)
      # get instrument metadata
      for keyname in nasa.MSL_KEY:
        key = nasa.MSL_KEY[keyname]
        if keyname in image[0:8]:
          meta['inst']      =  keyname
          meta['url']       = (key['url_prefix'] % solnum) + image + key['ext']
          meta['instname']  =  key['name']
          break
      meta['t'] = False
      
      if image[16] == "_":
        if image[17] in ['D', 'T']:
          meta['t'] = True;
      else:
        if image[16] == "I":
          meta['t'] = True;
        
      meta['id'] = image

      # Adds metadata to the feeds
      add_image(solnum, data[sol]["time"], meta)

      # remeber that we've seen it before
      r.sadd('msl-images', image)

