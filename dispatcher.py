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
        self.waiting_stack = []
        self.event = Event()

    def set_io_sys(self, io_sys):
        """Set the io subsystem."""
        self.io_sys = io_sys

    def add_process(self, process):
        """Add and start the process."""
        if len(self.runnable_stack) >= 2:
            self.runnable_stack[-2].event.clear()

        process.event.set()
        process.state = State.runnable
        self.runnable_stack.append(process)
        self.io_sys.allocate_window_to_process(process,
                                               len(self.runnable_stack) - 1)
        process.start()

    def dispatch_next_process(self):
        """Dispatch the process at the top of the runnable_stack."""
        stack_length = len(self.runnable_stack)
        if stack_length == 0:
            return
        else:
            self.runnable_stack[-1].event.set()
            if stack_length >= 2:
                self.runnable_stack[-2].event.set()

    def to_top(self, process):
        stack = self.runnable_stack
        """Move the process to the top of the runnable_stack."""
        if len(stack) == 1:
            return

        stack[-1].event.clear()  # stop current process
        original_pos = stack.index(process)
        self.io_sys.move_process(stack[original_pos], len(stack))

        # update model
        stack.append(stack.pop(original_pos))

        # shift everything
        for x in range(0, len(stack)):
            self.io_sys.move_process(stack[x], x)

        process.event.set()

    def pause_system(self):
        """Pause the currently running process.
        As long as the dispatcher doesn't dispatch another process this
        effectively pauses the system.
        """
        self.runnable_stack[-1].event.clear()
        self.runnable_stack[-2].event.clear()

    def resume_system(self):
        """Resume running the system."""
        self.runnable_stack[-1].event.set()
        self.runnable_stack[-2].event.set()

    def wait_until_finished(self):
        """Hang around until all runnable processes are finished."""
        while True:
            if len(self.runnable_stack) == 0:
                return

    def proc_finished(self, process):
        """Receive notification that "proc" has finished.
        Only called from running processes.
        """
        if not len(self.runnable_stack) == 0:
            self.runnable_stack.remove(process)
            self.io_sys.remove_window_from_process(process)
            for x in range(0, len(self.runnable_stack)):
                self.io_sys.move_process(self.runnable_stack[x], x)
            self.dispatch_next_process()

    def proc_waiting(self, process):
        """Receive notification that process is waiting for input."""
        # ...

    def process_with_id(self, id):
        """Return the process with the id."""
        for process in self.runnable_stack:
            if process.id == id:
                return process
        return None

    def kill_process(self, process):
        process.event.clear()
        self.runnable_stack.remove(process)  # remove desired process from stack
        self.io_sys.remove_window_from_process(process)  # update display to reflect remove
        process.state = State.killed
        # shift processes down
        for x in range(0, len(self.runnable_stack)):
            self.io_sys.move_process(self.runnable_stack[x], x)
