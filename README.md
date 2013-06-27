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
