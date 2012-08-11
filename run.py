#!/usr/bin/env python
import nasa
import json
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

#image_scraper = nasa.MSL_Images(vebose=False)
#data = image_scraper.get_images()
#print json.dumps(data)

data =  json.loads(open('cache.json', 'r').read())

for sol in data['sols']:
  for instrument in sol:
    print instrument['instrument_name']
    for image in instrument['images']:
      image_id = image['rawid']
      if not r.sismember('msl-images', image_id):
        r.sadd('msl-images', image_id)
        print "new image!!", image_id
