import threading
import time
import sys
import itertools

class Spinner:
    def __init__(self, message="Processing", delay=0.1, chars='|/-\\', file=sys.stdout):
        self.message = message
        self.delay = delay
        self.chars = chars
        self.file = file
        self.stop_running = threading.Event()
        self.spinner_generator = itertools.cycle(self.chars)
        self.thread = None

    def spinner_task(self):
        while not self.stop_running.is_set():
            self.file.write(f'\r{self.message} {next(self.spinner_generator)}')
            self.file.flush()
            time.sleep(self.delay)
        self.file.write('\r' + ' ' * (len(self.message) + 2) + '\r')
        self.file.flush()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self.spinner_task)
            self.thread.start()

    def stop(self):
        if self.thread is not None:
            self.stop_running.set()
            self.thread.join()
            self.thread = None

    def update_message(self, new_message):
        self.message = new_message
