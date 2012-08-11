import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_feeds():
  return r.smembers('msl-feeds')
