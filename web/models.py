import redis
import json
import datetime
import time

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_feeds():
  return r.smembers('msl-feeds')
  
def get_feed(feed):
  data = r.zrevrange(feed, 0, 5, withscores=True)
  
  feed_data = []
  
  for image in data:
    image_data  = json.loads(image[0])
    pub         = int(image[1])
    pub_dt      = datetime.datetime.fromtimestamp(pub).isoformat()
    rawid       = image_data["rawid"]
    
    url         = image_data["uri"]
    title       = "New Image %s" % rawid
    
    feed_data.append({"url": url, "id": rawid, "pub": pub_dt, "title": title})
    
  return feed_data 
