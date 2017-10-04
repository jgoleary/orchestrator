import pprint

class AbstractTask(object):

	def __init__(self, identifier, recurring, schedule, dependencies):
		# a string identifier for the concrete task. should be unique
		self.identifier = identifier
		# whether this is recurring or to be run once
		self.recurring = recurring
		# a spec for when the task is to be run
		self.schedule = schedule
		# the identifier(s) of task which must be run before this one
		self.dependencies = dependencies

	def __str__(self):
		class_name = self.__class__.__name__
		params = pprint.pformat(self.__dict__, width=1)
		s = '(Class: {},\nParams: {})'.format(class_name, params) 
		return s

	def run(self):
		# What the task actually does
		raise NotImplementedError()
