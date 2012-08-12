def render_feed_items_xml(items):
  xml = ""
  for item in items:
    xml += """  <entry>
    <author>
      <name>MSL Image Bot</name>
      <uri>FIXME</uri>
    </author>
    <title type="text">%(title)s</title>
    <id>%(id)s</id>
    <published>%(pub)s</published>
    <updated>%(pub)s</updated>

    <content type="html"><![CDATA[ <img src="%(uri)s" /> ]]></content>
    <link rel="enclosure" type="image/jpeg" href="%(uri)s" />
    <link rel="license" type="text/html" href="http://creativecommons.org/publicdomain/mark/1.0/" />
  </entry>\n""" % {"title": item["title"], "id": item["id"], "pub": item["pub"], "uri": item["url"]}
  return xml

def render_feed_xml(feed, items):
  title     = feed["title"]
  updated   = feed["updated"]
  feedid    = feed["feed"]
  items_xml = render_feed_items_xml(items)
  
  return """<?xml version="1.0" encoding="utf-8" ?>
<feed
  xmlns="http://www.w3.org/2005/Atom"
  xml:lang="en-US" >
  <title type="text">%(title)s</title>
	<updated>%(updated)s</updated>
	<id>%(id)s</id>
  %(items)s
</feed>""" % {"title": title, "updated": updated, "id": feedid, "items": items_xml}

def render_feeds_xml(feeds):
  xml = ""
  for feed in feeds:
    xml += '''  <feed href="feeds/%(feed)s.xml" 
        title="%(title)s" 
        updated="%(updated)s" />\n''' % {'feed': feed['feed'], 'title': feed['title'], 'updated': feed['updated']}
  return xml

def index_xml(feeds):
  feeds_xml = render_feeds_xml(feeds)
  return """<?xml version="1.0" encoding="utf-8" ?>
<feeds>
%s
</feeds>
""" % feeds_xml

def render_feeds_html(feeds):
  html = ""
  for feed in feeds:
    html += '  <li><h4><a href="feeds/%s.xml">%s</a></h4></li>' % (feed["feed"], feed["title"])
  return html

def render_latest_img(images):
  html = ""
  for uri in images:
    html += '<li class="span2"><a href="%(uri)s" class="thumbnail"><img src="%(uri)s" alt="latest MSL image" /></a></li>' % {"uri": uri}
  return html

def front_page(feeds, peekimg):

  feeds_html  = render_feeds_html(feeds)
  images_html = render_latest_img(peekimg)
  
  return """<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Latest images from MSL" />
  <meta name="author" content="natronics" />
  
  <!-- Bootstrap CSS -->
  <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet" />
  <style>
    #header {
      background: #eee;
      border-bottom: 3px solid #08c;
      padding-top: 40px;
      padding-bottom: 14px;
      margin-bottom: 30px;
    }
  </style>

  <!--Title-->
  <title>Latest MSL Images</title>
 </head>
 <body>
  
  <div id="header">
    <div class="container">
      <h1>Mars Science Laboratory RSS Feeds</h1>
    </div>
  </div>

  <div class="container">

    <div class="row">
      <div class="span3">
        <img src="img/msl_bot.png" />
      </div>
      <div class="span9">
        <div class="hero-unit">
          <h1>RSS from Mars!</h1>
          <p>
            A feed of only the latest photos from Mars Science Laboratory
          </p>
          <p>
            <small>Latest full res images from MSL:</small>
          </p>
            <ul class="thumbnails">
              %(latestimg)s
            </ul>
          <h2>Subscribe!</h2>
          <ul>
            <li>
              <h4><a href="feeds/msl-all-feed-nothumb.xml">Latest Images from MSL - Full Resolution Images Only</a></h4>
            </li>
          </ul>
          <p />
          <p>
            Get all the feeds below:
          </p>
        </div>
      </div>
    </div>
  
    <div class="row">
      <div class="span12">
          <h2>List of feeds:</h2>
          <ul>
            %(feeds)s
          </ul>
          
           <h2>XML list of feeds:</h2>
          <ul>
            <li><h4><a href="index.xml">List of Feeds (xml)</a></h4></li>
          </ul>
      </div>
    </div>
   
   <div class="footer">
     <hr />
     <p>Hand made artisanal code by <a href="https://twitter.com/natronics">@natronics</a> in Portland, Oregon.</p>
     <p>This site is not affiliated with NASA. Images credit: NASA/JPL</p>
   </div>
   
  </div>
  <script src="static/bootstrap/js/bootstrap.min.js"></script>
 </body>
</html>""" % {"feeds": feeds_html, "latestimg": images_html}
