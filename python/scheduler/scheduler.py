###############################################################

import sys
import time
import traceback
import threading
import Queue as queue

###############################################################

def _seconds():
    return time.time()

def _empty_function():
    pass

###############################################################

class SchedulerException(Exception):

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

###############################################################

class Runnable:
    def __init__(self, fn):
        self._fn = fn

    def run(self):
        self._fn()

###############################################################

class ScheduleFuture(Runnable):

    def __init__(self, fn, submit_time, initial_delay, delay):
        Runnable.__init__(self, fn)
        self._alive = True
        self._delay = delay
        self._last_run = None
        self._submit_time = submit_time
        self._initial_delay = initial_delay
        self._condition = threading.Condition()

    def is_periodic(self):
        with self._condition:
            return self._delay != None

    def is_alive(self):
        with self._condition:
            return self._alive

    def cancel(self):
        with self._condition:
            self._alive = False
            self._condition.notify_all()

    def wait(self, timeout=None):
        with self._condition:
            while self._alive:
                self._condition.wait(timeout)

    def _is_marked_as_run(self):
        with self._condition:
            return self._last_run != None

    def _get_timeout(self, now):
        with self._condition:
            if not self._is_marked_as_run():
                return ( self._submit_time + self._initial_delay ) - now

            if self.is_periodic():
                return ( self._last_run + self._delay ) - now

        return None

    def run(self):
        with self._condition:
            self._last_run = _seconds()

        Runnable.run(self)

###############################################################

class ScheduleFutureList:

    def __init__(self):
        self._list = []
        self._lock = threading.RLock()

    def get_next_timeout(self):
        with self._lock:
            now = _seconds()
            timeout = float('inf')
            for future in self._list:
                time = future._get_timeout(now)
                if time < timeout:
                    timeout = time

            if timeout == float('inf'):
                timeout = None
            return timeout


    def get_next_future(self):
        with self._lock:
            next = None
            now = _seconds()
            for future in self._list:
                time = future._get_timeout(now)
                if time <= 0:
                    next = future

            self._list.remove(next)
            return next

    def insert_future(self, future):
        with self._lock:
            self._list.append(future)

###############################################################

class ScheduledExecutor:

    def __init__(self, core_size):
        self._threads = []
        self._queue = queue.Queue()
        self._core_size = core_size
        self._schedule_list = ScheduleFutureList()

    def start(self):
        while len(self._threads) < self._core_size:
            thread = WorkerThread(self._queue, self._schedule_list)
            thread.start()
            self._threads.append(thread)

    def _internal_run(self):

        timeout = self._schedule_list.get_next_timeout()
        task = self.queue.get(True, 2)

    def submit(self, fn):
        if not isinstance(fn, Runnable):
            fn = Runnable(fn)
        self._queue.put_nowait(fn)
        return fn

    def schedule(self, fn, initial_delay, delay):
        now = _seconds()
        future = ScheduleFuture(fn, now, initial_delay, delay)
        self._queue.put_nowait(future)
        return future

    def delay(self, fn, delay):
        return self.schedule(fn, delay, None)

    def shutdown(self):
        for thread in self._threads:
            thread.cancel()

        for _ in range(self._core_size):
            self.submit(_empty_function)

        for thread in self._threads:
            thread.join()

    def wait(self, timeout=None):
        for thread in self._threads:
            thread.join(timeout)

###############################################################

class WorkerThread(threading.Thread):

    def __init__(self, queue, schedule_list):
        threading.Thread.__init__(self)
        self._running = True
        self._queue = queue
        self._schedule_list = schedule_list

    def _run_schedule_future(self):
        future = self._schedule_list.get_next_future()
        if future != None:
            self._execute(future)
            if future.is_periodic() and future.is_alive():
                self._schedule_list.insert_future(future)

    def _run_task(self, task):
        if isinstance(task, ScheduleFuture):
            self._schedule_list.insert_future(task)
        else:
            self._execute(task)

    def _execute(self, task):
        try:
            task.run()
        except:
            traceback.print_exc(file=sys.stderr)

    def cancel(self):
        self._running = False

    def run(self):
        while self._running:
            timeout = self._schedule_list.get_next_timeout()

            if timeout == None or timeout > 0:
                try:
                    task = self._queue.get(True, timeout)
                except queue.Empty:
                    continue
                self._run_task(task)
            else:
                self._run_schedule_future()
