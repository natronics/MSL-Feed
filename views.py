def render_feed_items_xml(items):
  xml = ""
  for item in items:
    xml += """  <entry>
    <author>
      <name>MSL Image Bot</name>
      <uri>http://mars.open-notify.org</uri>
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
  feeds = sorted(feeds)
  for feed in feeds:
    html += '  <li><h4><a href="http://fusion.google.com/add?source=atgs&feedurl=http%%3A//mars.open-notify.org/feeds/%(feed)s.xml"><img src="http://gmodules.com/ig/images/plus_google.gif" alt="Add to Google"></a> &nbsp; <a href="feeds/%(feed)s.xml">%(title)s</a></h4></li>' % {"feed": feed["feed"], "title": feed["title"]}
  return html


def render_latest_img(images):
  html = ""
  for uri in images:
    html += '<li class="span2"><a href="%(uri)s" class="thumbnail"><img src="%(uri)s" alt="latest MSL image" width="170" /></a></li>' % {"uri": uri}
  return html

def front_page(main_feeds, inst_feeds, peekimg):

  main_feeds_html  = render_feeds_html(main_feeds)
  inst_feeds_html  = render_feeds_html(inst_feeds)
  images_html      = render_latest_img(peekimg)
  
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
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-34037546-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
 </head>
 <body>
  
  <div id="header">
    <div class="container">
      <h1>Mars Science Laboratory RSS Feeds</h1>
      <a href="/about" class="btn btn-info" >About</a>
    </div>
  </div>

  <div class="container">

    <div class="row">
      <div class="span9">
        <div class="hero-unit">
          <h3>
            RSS Feeds of the latest photos from Mars Science Laboratory!
          </h3>
          <p>
            <small>Latest full res images from MSL:</small>
          </p>
            <ul class="thumbnails">
              %(latestimg)s
            </ul>
          <h2>Subscribe!</h2>
          <ul>
            <li>
              <h4>
                  <a href="/feeds/msl-all-feed-nothumb.xml">Latest Images from MSL - Full Resolution Images Only</a>
              </h4>
              <a href="http://fusion.google.com/add?source=atgs&feedurl=http%%3A//mars.open-notify.org/feeds/msl-all-feed-nothumb.xml">
                <img src="http://gmodules.com/ig/images/plus_google.gif" alt="Add to Google">
              </a>
            </li>
          </ul>
          <p />
          <p>
            Get all the feeds below:
          </p>
        </div>
      </div>
      <div class="span3">
        <img src="img/msl_bot.png" />
      </div>
    </div>
  
    <div class="row">
      <div class="span12">
          <h2>Main feeds:</h2>
          <ul>
            %(main_feeds)s
          </ul>
          
          <h2>Feeds by camera:</h2>
          <ul>
            %(inst_feeds)s
          </ul>
          
           <h2>XML list of feeds:</h2>
          <ul>
            <li><h4><a href="/index.xml">List of all feeds (xml)</a></h4></li>
          </ul>
      </div>
    </div>
   
   <div class="footer">
     <hr />
     <p>Hand made artisanal code by <a href="https://twitter.com/natronics">@natronics</a> in Portland, Oregon.</p>
     <p>This site is not affiliated with NASA. Images credit: NASA/JPL</p>
   </div>
   
  </div>
 </body>
</html>""" % {"main_feeds": main_feeds_html, "inst_feeds": inst_feeds_html, "latestimg": images_html}

def render_about_page():
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
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-34037546-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
 </head>
 <body>
  
  <div id="header">
    <div class="container">
      <h1>About Mars Science Laboratory RSS Feeds</h1>
      <a href="/" class="btn btn-info" >Home</a>
    </div>
  </div>

  <div class="container">
  
    <div class="row">
      <div class="span3 well" style="padding-top: 8px; padding-right: 0px; padding-bottom: 8px; padding-left: 0px;">
        <ul class="nav nav-list">
          <li class="nav-header">Table of Contents</li>
          <li><a href="#what">What is this?</a></li>
          <li><a href="#how">How do I use it?</a></li>
          <li><a href="#source">Source Code</a></li>
          <li><a href="#api">Other APIs</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </div>
      <div class="span8">
        <h2><a name="what"></a>What is this?</h2>
        <p>
          This is a set of public <a href="http://en.wikipedia.org/wiki/RSS">RSS</a>
          feeds dedicated to NASA's rover on Mars: <a href="http://en.wikipedia.org/wiki/Mars_Science_Laboratory">Mars Science Laboratory</a>
          (MSL). Nicknamed "Curiosity" MSL landed on Mars August 6th, 2012
          with a mission to drive around Gale Crater and learn about the geologic
          history of the planet Mars.
        </p>
        <p>
          The team at NASA responsible for MSL have been uploading images to 
          <a href="http://mars.jpl.nasa.gov/msl/multimedia/raw/">mars.jpl.nasa.gov/msl/multimedia/raw/</a>,
          but there is no way to know when a new image gets posted!
        </p>
        <p>
          This site watches these pages for you, and gathers all the new images into 
          an RSS feed that you can subscribe to with an RSS reader!  As soon as
          there is a new image posted the feeds are updated.
        </p>
        
        <p><br /></p>
        <h2><a name="how"></a>How do I use it?</h2>
        <p>
          Each feed link on the front page goes directly to the RSS formated file 
          that will update when there is a new image for that feed. Use an RSS reader
          and subscribe to the feed(s) you want.
        </p>
        <p>
          The main feeds will update when any new image is posted. There are also
          feeds for each camera on the rover. All feeds have a "full resolution only" 
          option that will ignore photos tagged as being a "thumbnail" by JPL. 
          The full resolution feeds may include subframe images, which are techncially 
          the full resolution availible, but not the full resolution of the particular
          camera.
        </p>
        <p>
          If you click one of the links you'll notice a bunch of unformated XML, that's okay!
          RSS works with a "reader" or "aggregator" that can understand an RSS feed.
          Google has a free one called <a href="http://google.com/reader/">google reader</a>
          if you already have an account! If you're using google 
          reader, just click the +Google button next to the one you want to subscribe to.
          If you use something else, look up how to add a new subscription and 
          follow the directions for your reader.
        </p>
        
        <p><br /></p>
        <h2><a name="source"></a>Source Code</h2>
        <p>
          The scraper in written in <a href="http://www.python.org/">python</a> using 
          <a href="http://redis.io/">redis</a> as a data store.
        </p>
        <p>
          All the code is availible on
          <a href="https://github.com/natronics/MSL-Feed" title="MSL-Feed on Github">Github</a>!
        </p>
        
        <p><br /></p>
        <h2><a name="api"></a>Other APIs</h2>
        <p>
          <a href="http://open-notify.org">open-notify.org</a> has some other space 
          APIs. Check out <a href="http://api.open-notify.org">api.open-notify.org</a>
          for more.
        </p>
        
        <p><br /></p>
        <h2><a name="contact"></a>Contact</h2>
        <p>
          You can find me on <a href="https://plus.google.com/u/0/113165147467813592377/posts">Google+</a>
          and <a href="https://twitter.com/natronics">twitter</a>. Or you can 
          email me at <a href="mailto:nathan@open-notify.org">nathan@open-notify.org</a>
        </p>
      </div>
    </div>
   
   <div class="footer">
     <hr />
     <p>Hand made artisanal code by <a href="https://twitter.com/natronics">@natronics</a> in Portland, Oregon.</p>
     <p>This site is not affiliated with NASA. Images credit: NASA/JPL</p>
   </div>
   
  </div>
 </body>
</html>"""
