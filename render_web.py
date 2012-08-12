#!/usr/bin/env python
import models
import views
import config


def render_front_page():
  feeds = models.get_feeds()
  peek  = models.get_latest_3()
  home = open(config.render_location + 'index.html', 'w')
  home.write(views.front_page(feeds, peek))

def render_feed_index():
  feeds = models.get_feeds()
  index = open(config.render_location + 'index.xml', 'w')
  index.write(views.index_xml(feeds))

def render_all_feeds():
  feeds = models.get_feeds()
  for feed in feeds:
    items = models.get_feed(feed["feed"])
    #meta = models.get_feed_metadata(feedname)
    #print meta
    feed_name = feed['feed']
    feed_file = open(config.render_location + config.feeds_location + feed_name + ".xml", 'w')
    feed_file.write(views.render_feed_xml(feed, items))

render_front_page()
render_feed_index()
render_all_feeds()
