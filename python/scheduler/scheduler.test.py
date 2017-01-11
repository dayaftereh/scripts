#!/usr/bin/python

import time
import latch
import unittest
import scheduler

#############################################################################

@unittest.skip("")
class ScheduledExecutorGeneral(unittest.TestCase):


    def setUp(self):
        self.executor = scheduler.ScheduledExecutor(2)

    def test_start(self):
        self.executor.start()

    def tearDown(self):
        self.executor.shutdown()

#############################################################################

@unittest.skip("")
class ScheduledExecutorRunnable(unittest.TestCase):

    def setUp(self):
        self.latch = latch.Latch(1)
        self.executor = scheduler.ScheduledExecutor(2)
        self.executor.start()

    def foo_fn(self):
        self.latch.count_down()

    def test_run(self):
        self.executor.submit(self.foo_fn)
        result = self.latch.wait(2.5)
        self.assertTrue(result)

    def tearDown(self):
        self.executor.shutdown()

#############################################################################

@unittest.skip("")
class ScheduledExecutorDelay(unittest.TestCase):

    def setUp(self):
        self.latch = latch.Latch(1)
        self.executor = scheduler.ScheduledExecutor(2)
        self.executor.start()

    def foo_fn(self):
        self.time = time.time()
        self.latch.count_down()

    def test_run(self):
        delay = 2.0
        start = time.time()

        self.executor.delay(self.foo_fn, delay)
        result = self.latch.wait(delay * 2.0)

        self.assertTrue(result)

        delta = self.time - start
        self.assertAlmostEqual(delay, delta, places=2)

    def tearDown(self):
        self.executor.shutdown()

#############################################################################

class ScheduledExecutorSchedule(unittest.TestCase):

    def setUp(self):
        self.times = []
        self.latch = latch.Latch(4)
        self.executor = scheduler.ScheduledExecutor(2)
        self.executor.start()

    def foo_fn(self):
        now = time.time()
        self.times.append(now)

        if len(self.times) >= 4:
            self.future.cancel()

        self.latch.count_down()

    def test_run(self):
        delay = 2.7
        initial_delay = 1.5
        start = time.time()

        self.future = self.executor.schedule(self.foo_fn, initial_delay, delay)
        result = self.latch.wait(initial_delay * 2.0 + delay * 4.0)

        time.sleep(5)

        self.assertTrue(result)
        self.assertEqual(len(self.times), 4)

        time0 = start + initial_delay
        self.assertAlmostEqual(time0, self.times[0], places=2)

        for i in range(1,4):
            t = start + initial_delay + delay * i
            self.assertAlmostEqual(t, self.times[i], places=2)

    def tearDown(self):
        self.executor.shutdown()

#############################################################################

def main():
    unittest.main()

if __name__ == '__main__':
    main()
