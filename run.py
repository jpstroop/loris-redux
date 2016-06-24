#!/usr/bin/env python
from loris.loris_app import create_tornado_application
from tornado.ioloop import IOLoop

if __name__ == "__main__":
    app = create_tornado_application()
    app.listen(8888)
    IOLoop.current().start()
