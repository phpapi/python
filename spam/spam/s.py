import sys, logging, os
import multiprocessing as mp

import json

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.process

import ahocorasick

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from tornado.options import define, options

def name2fn(name):
  return 'words-%s.txt' % name

class Filter():
  _forest = {}

  @staticmethod
  def build(name):
    tree = None
    count = 0
    for line in open(name2fn(name), 'rb').readlines():
      s = line.strip('\r\n')
      if s: # empty check
        if 0 == count:
          tree = ahocorasick.KeywordTree()
        tree.add(s)
        count = count + 1
    if count != 0:
      tree.make()
    return tree

  @staticmethod
  def get_or_build_tree(name):
    x = Filter._forest.get(name)
    if not x:
      x = Filter.build(name)
      if x:
        Filter._forest[name] = x
    return x

  @staticmethod
  def check(name, content):
    x = Filter.get_or_build_tree(name)
    if x:
      return x.findall_long(content)
    else:
      return [];

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
class GetHandler(tornado.web.RequestHandler,Filter):
    def get(self, name=None, status=None):
		try:
		  words=open(name2fn(name), 'rb').read()
		except:
			words = ''
		#word = words.encode("utf-8")
		#word = words.split('\n')
		#self.write(words)
		word = words.split("\n".encode("utf-8"))
		s = json.dumps(word)
		self.write(s)
		#content = words.encode("utf-8")
		#m = Filter.check(name, content)
		#s = json.dumps([i for i in m])
		#self.write(s)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/get/([^/]+)", GetHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8889)
    tornado.ioloop.IOLoop.instance().start()
