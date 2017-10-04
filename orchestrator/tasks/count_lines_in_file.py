from random import randrange

from tasks.abstract_task import AbstractTask

'''
Mock task for counting the lines in a specified file
'''
class CountLinesInFile(AbstractTask):
	def run(self):
		print("File has {} lines!".format(randrange(100)))
