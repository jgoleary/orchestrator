from collections import defaultdict

#phony db
mock_db = defaultdict(list)

class Session(object):

	@staticmethod
	def find_last_by_id(identifier):
		#return the last task with that identifier
		if identifier in mock_db:
			return mock_db[identifier][-1]

		return None

	@staticmethod
	def persist(model):
		mock_db[model.identifier].append(model)


class TaskRun(object):
	def __init__(self, identifier, start_time, end_time=None):
		self.identifier = identifier
		self.start_time = start_time
		self.end_time = end_time
