import redis
import json
import datetime
import time

r = redis.StrictRedis(host='localhost', port=6379, db=0)

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

    instrument  = image_data["instrument"].split('(')[0].strip()
    url         = image_data["uri"]
    title       = "New Image fount on %s from %s" % ("DT", instrument)

    feed_data.append({"url": url, "id": rawid, "pub": pub_dt, "title": title})

  return feed_data

def get_feed_metadata(feed):
  title = r.get(feed + "-name")
  
  data = r.zrevrange(feed, 0, 0, withscores=True)
  
  last_updated = datetime.datetime.fromtimestamp(int(data[0][1])).isoformat()
  
  return {"title": str(title), "updated": last_updated}
