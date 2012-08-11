#!/usr/bin/env python
import nasa
import json

image_scraper = nasa.MSL_Images(vebose=False)
data = image_scraper.get_images()

print json.dumps(data)
