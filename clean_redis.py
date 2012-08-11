#!/usr/bin/env python
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

feeds = r.smembers('msl-feeds')

for feed in feeds:
  print "deleting", feed
  r.delete(feed)

print "deleting msl-feeds"
r.delete('msl-feeds')

print "deleting msl-images"
r.delete('msl-images')
