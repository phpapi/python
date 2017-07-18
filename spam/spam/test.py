import sys, logging, os
import multiprocessing as mp

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.process
from tornado.options import define, options
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("You requested the main page")

class StoryHandler(tornado.web.RequestHandler):
    def get(self, story_id):
        self.write("You requested the story " + story_id)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/story/([0-9]+)", StoryHandler),
])

if __name__ == "__main__":
  options.log_file_prefix = "filterserver.log"
  options.log_file_num_backups = 10
  options.log_file_max_size = 20 * 1000 * 1000
  options.log_to_stderr = False
  logging.getLogger().setLevel(logging.INFO)
  options.parse_command_line()


