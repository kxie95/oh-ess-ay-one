# A1 for COMPSCI340/SOFTENG370 2015
# Prepared by Robert Sheehan
# Modified by Karen Xie (kxie094)

# You are not allowed to use any sleep calls.

from threading import Lock, Event
from process import State


class Dispatcher():
    """The dispatcher."""

    MAX_PROCESSES = 8

    def __init__(self):
        """Construct the dispatcher."""
        self.runnable_stack = []
        self.event = Event()

    def set_io_sys(self, io_sys):
        """Set the io subsystem."""
        self.io_sys = io_sys

    def add_process(self, process):
        """Add and start the process."""
        if not len(self.runnable_stack) == 0:
            self.runnable_stack[-1].event.clear()

        process.event.set()
        process.state = State.runnable
        self.runnable_stack.append(process)
        self.io_sys.allocate_window_to_process(process,
                                               len(self.runnable_stack) - 1)
        process.start()

    def dispatch_next_process(self):
        """Dispatch the process at the top of the runnable_stack."""
        self.runnable_stack[-1].event.set()

    def to_top(self, process):
        """Move the process to the top of the runnable_stack."""
        self.runnable_stack[-1].event.clear()

        self.runnable_stack.remove(process)
        self.runnable_stack.append(process)
        process.event.set()

    def pause_system(self):
        """Pause the currently running process.
        As long as the dispatcher doesn't dispatch another process this
        effectively pauses the system.
        """
        self.runnable_stack[-1].event.clear()

    def resume_system(self):
        """Resume running the system."""
        self.runnable_stack[-1].event.set()

    def wait_until_finished(self):
        """Hang around until all runnable processes are finished."""
        # ...

    def proc_finished(self, process):
        """Receive notification that "proc" has finished.
        Only called from running processes.
        """
        # ...

    def proc_waiting(self, process):
        """Receive notification that process is waiting for input."""
        # ...

    def process_with_id(self, id):
        """Return the process with the id."""
        for process in self.runnable_stack:
            if process.id == id:
                return process
        return None
