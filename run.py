#!/usr/bin/env python
from loris.loris_app import LorisApp
from tornado.ioloop import IOLoop

if __name__ == "__main__":
    # TODO: grab debug here or make the loris_app module executable as well.
    app = LorisApp.create_tornado_application()
    app.listen(8888)
    IOLoop.current().start()
