#!/usr/bin/env python
import web
import view
import models

urls = (
  '/',                'Index',
  '/index.xml',       'Feeds_Index',
  '/feeds/(.+).xml',  'Feed', 
)

class Index:
  def GET(self):
    return view.render.base("", title="MSL Feeds")

class Feeds_Index:
  def GET(self):
    feed_urls = models.get_feeds()
    feed_index = view.render.feed_index(feed_urls)
    return view.render.base_xml(feed_index)

class Feed:
  def GET(self, feedname):
    items = view.render.feed_entry("")
    feed = view.render.feed("","",items)
    return view.render.base_xml(feed)

if __name__ == "__main__":
  app = web.application(urls, globals())
  app.internalerror = web.debugerror
  app.run()
