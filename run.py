#!/usr/bin/env python
from loris.app import App
from tornado.ioloop import IOLoop

if __name__ == "__main__":
    # load configs here and pass to create_app?
    app = App.create()
    app.listen(8888)
    IOLoop.current().start()
