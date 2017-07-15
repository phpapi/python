#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys, logging, os
import multiprocessing as mp

import json

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.process

import ahocorasick

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

# cross process dict
# name => version
gd = mp.Manager().dict({})

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

class KeywordsUpdateHandler(tornado.web.RequestHandler):
  def get(self, name=None, status=None):
    try:
      words=open(name2fn(name), 'rb').read()
    except:
      words = ''
    self.render("form.html", words=words, name=name, status=status)

  def post(self, name=None):
    content = self.get_argument("words")
    # post的textarea居然是\r\n，去掉\r
    content = content.replace("\r", "")
    status = "Update words succeded"
    try:
      with open(name2fn(name), "wb") as f:
        f.write(content.encode("utf8"))
        global gd
        if name in gd:
          gd[name] += 1
        else:
          gd[name] = 1
    except Exception,e:
      status = str(e)
    self.get(name, status)

class FilterHandler(tornado.web.RequestHandler, Filter):
  def get(self, name=None, status=None):
    self.redirect('/update/%s' % name)

  ld = {}

  def check_or_rebuild(self, name):
    # if all None, do nothong
    # if not match, rebuild
    global gd

    if name not in gd and name not in self.ld:
      return

    if name not in self.ld or gd[name] != self.ld[name]:
      try:
        print('try rebuild', os.getpid())
        del Filter._forest[name]
      except:
        pass

      self.ld[name] = gd[name]

  def post(self, name=None):
    if name is None:
      name = 'all'
    
    self.check_or_rebuild(name)

    content = self.get_argument("words").encode("utf8")
    m = Filter.check(name, content)
    s = json.dumps([i for i in m])
    self.write(s)

class GetHandler(tornado.web.RequestHandler,Filter):
    def get(self, name=None, status=None):
		try:
		  words=open(name2fn(name), 'rb').read()
		except:
			words = ''
		word = words.split("\n".encode("utf-8"))
		s = json.dumps(word)
		self.write(s)

def main():
  settings = dict(
    # cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    # login_url="/auth/login",
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    # static_path=os.path.join(os.path.dirname(__file__), "static"),
    # xsrf_cookies=True,
    debug=False,
    gzip=True,
    # autoescape=None,
  )
  app = tornado.web.Application([
    (r"/", FilterHandler),
    (r"/check/([^/]+)", FilterHandler),
    (r"/get/([^/]+)", GetHandler),
    (r"/update/([^/]+)", KeywordsUpdateHandler)
  ], **settings)

  sock = tornado.netutil.bind_sockets(options.port, address='0.0.0.0')
  if not settings['debug']:
    tornado.process.fork_processes(4)

  server = tornado.httpserver.HTTPServer(app)
  server.add_sockets(sock)

  tornado.ioloop.IOLoop.instance().start()



if __name__ == "__main__":
  options.log_file_prefix = "filterserver.log"
  options.log_file_num_backups = 10
  options.log_file_max_size = 20 * 1000 * 1000
  options.log_to_stderr = False
  logging.getLogger().setLevel(logging.INFO)
  options.parse_command_line()

  main()
