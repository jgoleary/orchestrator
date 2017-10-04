import argparse
import logging
import yaml
import threading
import time
import sys

import executor
from config import processor

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', 
	level=logging.INFO)

def read_config():
	parser = argparse.ArgumentParser()
	parser.add_argument('config_filename',
		help='A configuration file describing the tasks to be run.')

	args = parser.parse_args()

	with open(args.config_filename) as f:
		config = yaml.load(f)

	logging.info('Read task configuration from ' + args.config_filename)

	return config

def run_task_loop(tasks):

	stop = threading.Event()
	task_loop_thread = threading.Thread(target=task_loop, args=(tasks,stop))
	#task_loop_thread.daemon = True

	task_loop_thread.start()

	try:
		task_loop_thread.join()
	except KeyboardInterrupt:
		logging.info('Caught KeyboardInterrupt -- terminating task loop.')
		stop.set()

def task_loop(tasks, stop):
	while not stop.is_set():
		# run every 1 second
		next_call = time.time() + 1

		executor.run_pending_tasks(tasks)
		#go through tasks, check for what's pending
		time.sleep(next_call - time.time())

def main():
	config = read_config()
	tasks = processor.instantiate_tasks(config)

	run_task_loop(tasks)

if __name__ == '__main__':
	main()