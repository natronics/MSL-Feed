import web
import feedparser
import random

render = web.template.render('templates/', cache=False, globals={})
render._keywords['globals']['render'] = render
