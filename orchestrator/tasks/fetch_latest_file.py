from tasks.abstract_task import AbstractTask

'''
Mock task for going to a specified path and
watching for a newly arriving file.
'''
class FetchLatestFile(AbstractTask):
	def __init__(self, path, **kwargs):
		super().__init__(**kwargs)
		self.path = path

	def run(self):
		print('Found new file in ' + self.path)
