MSL-Feed
========

Feed of images from MSL data

Now live at [mars.open-notify.org](http://mars.open-notify.org)

Subscribe to an RSS feed of the MSL images!


To run yourself, have python and redis running.

Edit config.py and set your redis server settings

Run:

    $ ./scrape_latest.py

Genorate html

    $ ./render_web.py


To start over:

    $ ./clean_redis.py
