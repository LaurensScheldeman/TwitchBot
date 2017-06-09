from threading import Timer
import time

class InfiniteTimer():
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, seconds, target, target_arguments=None):
        # Initiate a timer, but don't start the timer yet
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.target_arguments = target_arguments
        self.thread = None

    def _handle_target(self):
        if self.is_running:
            self.is_running = False
            if self.target_arguments:
                self.target(self.target_arguments)
            else:
                self.target()
        self._start_timer()

    def _start_timer(self):
        if self._should_continue: # Code could have been running when cancel was called.
            self.is_running = True
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
        else:
            print("WARNING: Timer already started or running, please wait if you're restarting.")

    def stop(self):
        if self.thread is not None:
            self._should_continue = False # Just in case thread is running and cancel fails.
            self.thread.cancel()
            self.is_running = False
        else:
            print("WARNING: Timer never started or failed to initialize.")
