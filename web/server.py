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
    feeds = models.get_feeds()
    return view.render.base(view.render.front_page(feeds), title="MSL Feeds")

class Feeds_Index:
  def GET(self):
    feeds = models.get_feeds()
    feed_index = view.render.feed_index(feeds)
    return view.render.base_xml(feed_index)

class Feed:
  def GET(self, feedname):
    f = models.get_feed(feedname)
    meta = models.get_feed_metadata(feedname)
    items = view.render.feed_entry(f)
    feed = view.render.feed(meta["title"], meta["updated"], feedname, items)
    return view.render.base_xml(feed)

if __name__ == "__main__":
  app = web.application(urls, globals())
  app.internalerror = web.debugerror
  app.run()
