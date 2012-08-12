import redis
import json
import datetime
import time
import config

r = redis.StrictRedis(host=config.redis_host, port=config.redis_port, db=config.redis_db)

def get_feeds():
  feed_data = []
  feeds = r.smembers('msl-feeds')
  for feed in feeds:
    meta = get_feed_metadata(feed)
    feed_data.append({"feed": feed, "title": meta['title'], "updated": meta['updated']})
  return feed_data

def get_feed(feed):
  data = r.zrevrange(feed, 0, 30, withscores=True)

  feed_data = []

  for image in data:
    image_data  = json.loads(image[0])
    pub         = int(image[1])
    pub_dt      = datetime.datetime.fromtimestamp(pub).isoformat()
    rawid       = image_data["rawid"]
    
    pub_title   = datetime.datetime.fromtimestamp(pub).strftime("%B %d")
    instrument  = image_data["instrument"].split('(')[0].strip()
    url         = image_data["uri"]
    title       = "New Image uploaded on %s from %s" % (pub_title, instrument)
    title       = str(title).replace("&", "&amp;")

    feed_data.append({"url": url, "id": rawid, "pub": pub_dt, "title": title})

  return feed_data

def get_feed_metadata(feed):
  title = r.get(feed + "-name")
  
  data = r.zrevrange(feed, 0, 0, withscores=True)
  
  last_updated = datetime.datetime.fromtimestamp(int(data[0][1])).isoformat()
  
  title = str(title).replace("&", "&amp;")
  return {"title": title, "updated": last_updated}

def get_latest_3():
  data = r.zrevrange('msl-all-feed-nothumb', 0, 2)
  urls = []
  for image in data:
    image_data  = json.loads(image)
    urls.append( image_data["uri"] )
  return urls
