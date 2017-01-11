# Scheduler

Scheduler is a python libraries with the functionally to execute tasks in a thread pool instantly, after a given delay, or to execute periodically.
The Scheduler starts a group of threads as workers to execute the give tasks.
The implementation is based on the [ScheduledThreadPoolExecutor](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/ScheduledThreadPoolExecutor.html) from Java.
Inside the scheduler use a blocking queue for reducing the resource usage and a scheduler list to execute task closely to the delay or period.

## Usage
```python
import scheduler
# ...
# creates a ScheduledExecutor with to threads
executor = scheduler.ScheduledExecutor(2)
# start the executor
executor.start()
# ...
# function to execute
def foo():
  print 'foo'

# executes the function 'foo' instently
runnable = executor.submit(foo)

# ...
# executes the function 'foo' once after 2.5 seconds
future = executor.delay(foo, 2.5)

# ...
# executes the function 'foo' after 2.0 seconds and then periodically every 3.0 seconds
future = executor.schedule(foo, 2.0, 3.0)
# stops the execution from function 'foo'
future.cancel()
```
