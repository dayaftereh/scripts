import Queue as queue
import sys
import threading
import time
import traceback

import latch


###############################################################

def _seconds():
    return time.time()


def _empty_function():
    pass


###############################################################

class SchedulerException(Exception):
    def __init__(self, message, *args):
        self.args = args
        self.message = message

    def _to_string(self):
        if self.args:
            return str(self.message) % self.args
        return str(self.message)

    def __str__(self):
        return self._to_string()


###############################################################

class Runnable:
    def __init__(self, fn):
        self._fn = fn
        self._future = Future()

    @property
    def get_future(self):
        return self._future

    def run(self):
        if self._future.is_done():
            raise SchedulerException("can't execute function [ %s ], because already executed", self._fn)

        if not self._future.is_canceled():
            self._fn()

        self._future.notify_all()


###############################################################

class Future:
    def __init__(self):
        self._hooks = []
        self._done = False
        self._canceled = False
        self._latch = latch.Latch(1)
        self._lock = threading.RLock()

    @property
    def is_done(self):
        with self._lock:
            return self._done

    def is_canceled(self):
        with self._lock:
            return self._canceled

    def cancel(self):
        with self._lock:
            self._canceled = True

    def hook(self, hook):
        with self._lock:
            self._hooks.append(hook)

    def notify_all(self):
        with self._lock:
            if self._done:
                return
            self._done = True
            for hook in self._hooks:
                hook()

        self._latch.count_down()

    def wait(self, timeout=None):
        return self._latch.wait(timeout)


###############################################################

class ScheduleRunnable(Runnable):
    def __init__(self, fn, initial_delay, delay):
        Runnable.__init__(self, fn)
        self._delay = delay
        self._last_run = None
        self._lock = threading.RLock()
        self._submit_time = _seconds()
        self._initial_delay = initial_delay

    def is_periodic(self):
        with self._lock:
            return self._delay is not None

    def is_marked_as_run(self):
        with self._lock:
            return self._last_run is not None

    def get_timeout(self, now):
        if not self.is_marked_as_run():
            return (self._submit_time + self._initial_delay) - now

        if self.is_periodic():
            return (self._last_run + self._delay) - now

        return None

    def run(self):
        with self._lock:
            self._last_run = _seconds()
        Runnable.run(self)


###############################################################

class ScheduleTaskList:
    def __init__(self):
        self._list = []
        self._lock = threading.RLock()

    def get_next_timeout(self):
        with self._lock:
            return self._next_timeout()

    def _next_timeout(self):
        timeout = float('inf')
        current_time = _seconds()

        for task in self._list:
            task_timeout = task.get_timeout(current_time)
            if task_timeout < timeout:
                timeout = task_timeout

        if timeout == float('inf'):
            timeout = None

        return timeout

    def get_next_task(self):
        with self._lock:
            return self._next_task()

    def _next_task(self):
        next_task = None
        current_time = _seconds()

        for task in self._list:
            task_timeout = task.get_timeout(current_time)
            if task_timeout <= 0:
                next_task = task

        self._list.remove(next_task)
        return next_task

    def append_task(self, task):
        with self._lock:
            self._list.append(task)


###############################################################

class ScheduledExecutor:
    def __init__(self, core_size):
        self._threads = []
        self._running = False
        self._queue = queue.Queue()
        self._core_size = core_size
        self._lock = threading.RLock()
        self._latch = latch.Latch(core_size)
        self._task_list = ScheduleTaskList()

    def start(self):
        with self._lock:
            self._running = True

            while len(self._threads) < self._core_size:
                thread = ScheduledExecutorThread(self._latch, self._queue, self._task_list)
                self._threads.append(thread)
                thread.start()

    def get_core_size(self):
        with self._lock:
            return len(self._threads)

    def is_running(self):
        with self._lock:
            return self._running

    def _valid_is_running(self):
        if not self._running:
            raise SchedulerException('submission failed, because scheduled executor is not running')

    def submit(self, fn):
        with self._lock:
            self._valid_is_running()

            if not isinstance(fn, Runnable):
                fn = Runnable(fn)

            self._queue.put_nowait(fn)
            return fn.get_future()

    def schedule(self, fn, initial_delay, delay):
        with self._lock:
            self._valid_is_running()

            runnable = ScheduleRunnable(fn, initial_delay, delay)

            self._queue.put_nowait(runnable)
            return runnable.get_future()

    def delay(self, fn, delay):
        return self.schedule(fn, delay, None)

    def shutdown(self):
        with self._lock:
            if not self._running:
                return
            self._running = False

            for thread in self._threads:
                thread.cancel()

            for _ in range(self._core_size):
                self.submit(_empty_function)

    def wait(self, timeout=None):
        return self._latch.wait(timeout)


###############################################################

class ScheduledExecutorThread(threading.Thread):
    def __init__(self, shutdown_latch, task_queue, schedule_list):
        threading.Thread.__init__(self)
        self._running = True
        self._queue = task_queue
        self._schedule_list = schedule_list
        self._shutdown_latch = shutdown_latch

    def _execute_schedule_runnable(self):
        runnable = self._schedule_list.get_next_task()
        if runnable is not None:
            ScheduledExecutorThread._execute(runnable)
            if runnable.is_periodic() and not runnable.is_done():
                self._schedule_list.insert_future(runnable)

    def _execute_runnable(self, runnable):
        if isinstance(runnable, ScheduleRunnable):
            self._schedule_list.insert_future(runnable)
        else:
            ScheduledExecutorThread._execute(runnable)

    @staticmethod
    def _execute(task):
        try:
            task.run()
        except:
            traceback.print_exc(file=sys.stderr)

    def cancel(self):
        self._running = False

    def _next_runnable(self, timeout):
        try:
            runnable = self._queue.get(True, timeout)
            return runnable
        except queue.Empty:
            return None

    def run(self):
        while self._running:
            timeout = self._schedule_list.get_next_timeout()

            if timeout is None or timeout > 0:
                runnable = self._next_runnable(timeout)
                if runnable is not None:
                    self._execute_runnable(runnable)
            else:
                self._execute_schedule_runnable()

        self._shutdown_latch.count_down()
