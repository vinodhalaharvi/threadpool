#===============================================================================
# Script provided by Vinod Halaharvi, email: vinod.halaharvi@gmail.com, vinod.halaharvi@rtpnet.net
# RTP Network Services, Inc. / 904-236-6993 ( http://www.rtpnet.net ) # DESCRIPTION:  
#===============================================================================
import os, sys, threading, time, Queue
import sys, os, time, re, threading, Queue
import subprocess, shlex

__all__ = ["ThreadPool", "TaskHandler", "Task"]
MAXNUMTHREADS = 100 


class TaskHandler(object):
	"""docstring for TaskHandler"""
	def __init__(self, cmdline):
		super(TaskHandler, self).__init__()
		self.cmdline = cmdline

	def handle_task(self, *args):
		"""docstring for handle_line"""
		(threadId, threadName, taskName) = args
		self.proc = subprocess.Popen(shlex.split(self.cmdline),
					 stdout = subprocess.PIPE,
					 stderr = subprocess.PIPE,
					 env = os.environ
				)
		stdout, stderr = self.proc.communicate()
		if stderr:
			print stderr
		print stdout,
		self.proc.stderr.close()
		self.proc.stdout.close()
		status = self.proc.returncode
		
class Task(object):
	"""docstring for Task"""
	def __init__(self, taskName, handler):
		super(Task, self).__init__()
		self.taskName = taskName
		self.handler = handler


class _WorkThread(threading.Thread):
	"""docstring for _WorkThread"""
	def __init__(self, threadId, threadName):
		super(_WorkThread, self).__init__()
		self.threadId = threadId
		self.threadName = threadName
		self.sleep = 2
		self.queue = None
		self.lock = None
	def setThreadName(self, threadName):
		"""docstring for threadName"""
		self.threadName = threadName
	def getThreadName(self):
		"""docstring for getThreadName"""
		return getThreadName
	def setSleep(self, sleep):
		"""docstring for setSleep"""
		self.sleep = sleep
	def getSleep(self):
		"""docstring for getSleep"""
		return self.sleep
	def setup(self, queue, lock):
		"""docstring for setup"""
		self.queue = queue
		self.lock = lock
		
	def run(self):
		"""docstring for run"""
		try:
			q = None
			while not self.queue.empty():
				with self.lock:
					q = self.queue.get()
				if q:
					q.handler.handle_task(self.threadName, self.threadId, q.taskName)
					time.sleep(self.sleep)
		except Exception, e:
			raise e

class ThreadPool(object):
	"""docstring for ThreadPool"""
	def __init__(self, tasks, numthreads, sleep=1):
		super(ThreadPool, self).__init__()
		print "Starting Main Thread .. " 
		lock = threading.Lock()
		queue = Queue.Queue()
		self.numthreads = numthreads
		self.sleep = sleep
		assert self.numthreads <= MAXNUMTHREADS
		self.tasks = tasks

		with lock:
			# create task that want the thread pool to carry out
			for task in self.tasks:
				queue.put(task)

		threadList = []
		# create thread list
		for i in range(self.numthreads):
			t = _WorkThread(i, "Thread" + str(i))
			t.setup(queue, lock)
			t.setSleep(self.sleep)
			threadList.append(t)

		# start threads
		for t in threadList:
			t.start()

		# join for thread if need be
		for t in threadList:
			t.join()

		print "All threads done processing .. " 
		print "Ending Main thread .. " 




'''
Some examples are handlers are as shown below
class TaskHandler(object):
	"""docstring for TaskHandler"""
	def __init__(self, *args):
		super(TaskHandler, self).__init__()
		self.args = args
		self.cmdline = args

	def taskSetup(self, cmdline):
		"""docstring for taskSetup"""
		self.cmdline = cmdline

	def handle_task(self, *args):
		"""docstring for handle_line"""
		(threadId, threadName, taskName) = args
		self.proc = subprocess.Popen(shlex.split(self.cmdline),
					 stdout = subprocess.PIPE,
					 stderr = subprocess.PIPE,
					 env = os.environ
				)
		stdout, stderr = self.proc.communicate()
		if stderr:
			print stderr
		print stdout,
		self.proc.stderr.close()
		self.proc.stdout.close()
		status = self.proc.returncode
		



# one way to create a TaskHandler is to override the default TaskHandler class 
# and override the handle_task() 
class MyTaskHandler(TaskHandler):
	"""docstring for MyTaskHandler"""
	def __init__(self, *args):
		super(MyTaskHandler, self).__init__(*args)
		self.args = args
	def handle_task(self, *args):
		(threadId, threadName, taskName) = args
		"""docstring for handle_task"""
		print " Performing .. %s .. " % str(self.args)

# Sample Task class
class Task(object):
	"""docstring for Task"""
	def __init__(self, taskName, handler):
		super(Task, self).__init__()
		self.taskName = taskName
		self.handler = handler

# Easiest is to just inherit
class MyTask(Task): pass


#Sample main block of code
if __name__ == '__main__':
	#ThreadPool(numthreads, [handlers])
	"""	
		# Sample Usage
		for i in range(10):
			tasks.append(Task(" Task", TaskHandler())))
		# ThreadPool([tasks], numOfThreads, sleepInterval)
		ThreadPool(tasks, 10, 2)
	"""
	tasks = []
	for i in range(100):
		tasks.append(Task(" Task", MyTaskHandler("hostname")))
	ThreadPool(tasks, 10, 2)


# you can just inherit from TaskHandler class 
class MyTaskHandler(TaskHandler): pass

#main block of code
if __name__ == '__main__':
	tasks = []
	#ThreadPool(numthreads, [handlers])
	for line in sys.stdin.readlines():
		t = Task("Task", MyTaskHandler("hostname"))
		tasks.append(t)
	# ThreadPool([tasks], numOfThreads, sleepInterval)
	ThreadPool(tasks, 10, 2)
'''
