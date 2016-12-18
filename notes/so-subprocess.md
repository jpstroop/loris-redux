http://stackoverflow.com/q/40352825/714478

Greetings SO,

Within a Python 3 web application, I need to shell out to a command line utility that processes an image, writes its output to a named pipe (fifo), and then parse that output (the content of the pipe) into a PIL/Pillow Image. Here's the basic flow (and working code so long and there are no errors!):

<!-- language: python -->

    from os import mkfifo
    from os import unlink
    from PIL import Image
    from subprocess import DEVNULL
    from subprocess import PIPE
    from subprocess import Popen

    fifo_path = '/tmp/myfifo.bmp'
    cmd = '/usr/bin/convert -resize 100 /path/to/some.tif ' + fifo_path
    # make a named pipe
    mkfifo(fifo_path)
    # execute
    proc = Popen(cmd, stdout=DEVNULL, stderr=PIPE, shell=True)
    # parse the image
    pillow_image = Image.open(fifo_path)
    # finish the process:
    proc_exit = proc.wait()
    if proc_exit != 0:
        print(proc_exit)
        for line in proc.stderr.read().splitlines():
            print(line.decode('utf-8'))
    # remove the pipe:
    unlink(fifo_path)
    # just for proof:
    pillow_image.show()

(I've replaced the utility I actually have to work with with ImageMagick in the example above, just because you're not likely to have it--it doesn't influence the problem at all.)

This works great in most circumstances, and I can handle most exceptions (left out above for clarity), but there's one case I can't manage to work out how to handle, which is what to do if something goes wrong in the shellout, resulting in an empty pipe e.g. if the image doesn't exist or is corrupt for some reason, e.g.:

<!-- language: python -->

    fifo_path = '/tmp/myfifo.bmp'
    cmd = '/usr/bin/convert -resize 100 /path/to/some/bad_or_missing.tif ' + fifo_path
    # make a named pipe
    mkfifo(fifo_path)
    # execute
    proc = Popen(cmd, stdout=DEVNULL, stderr=PIPE, shell=True)
    # parse the image
    pillow_image = Image.open(fifo_path) # STUCK
    ...

The application just hangs here, and because I can't get to `proc_exit = proc.wait()` I can't set `timeout` (e.g. `proc_exit = proc.wait(timeout=2)`), which is what I'd normally do.

I've tried wrapping the whole business in a context manager, similar to [this answer](http://stackoverflow.com/a/22348885/714478), but that recipe is not thread safe, which is a problem, and I can't find a threading or multiprocessing solution that gives me access to the PIL/Pillow Image instance when I join the thread or process (not my strong suit, but something like this):

<!-- language: python -->

    from multiprocessing import Process
    from os import mkfifo
    from os import unlink
    from PIL import Image
    from subprocess import DEVNULL
    from subprocess import PIPE
    from subprocess import Popen

    def do_it(cmd, fifo_path):
        mkfifo(fifo_path)
        # I hear you like subprocesses with your subprocesses...
        sub_proc = Popen(cmd, stdout=DEVNULL, stderr=PIPE, shell=True)
        pillow_image = Image.open(fifo_path)
        proc_exit = sub_proc.wait()
        unlink(fifo_path)

    fifo_path = '/tmp/myfifo.bmp'
    cmd = '/usr/bin/convert -resize 100 /path/to/some/bad_or_missing.tif ' + fifo_path
    proc = Process(name='do_it', target=worker, args=(cmd, fifo_path))
    proc.daemon = True
    proc.start()
    proc.join(timeout=3) # I can set a timeout here
    # Seems heavy anyway, and how do I get pillow_image back for further work?
    pillow_image.show()

Hopefully these illustrate my problem and what I've tried. Thanks in advance.
