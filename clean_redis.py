#!/usr/bin/env python
import redis
import config

r = redis.StrictRedis(host=config.redis_host, port=config.redis_port, db=config.redis_db)

feeds = r.smembers('msl-feeds')

for feed in feeds:
  print "deleting", feed
  r.delete(feed)
  
  print "deleting", feed + "-name"
  r.delete(feed + "-name")

print "deleting msl-feeds"
r.delete('msl-feeds')

print "deleting msl-images"
r.delete('msl-images')
