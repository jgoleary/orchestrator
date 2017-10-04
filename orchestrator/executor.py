import logging
from datetime import datetime

from utils import time
from models import Session, TaskRun

def run_pending_tasks(tasks):
	for task_id, task in tasks.items():
		
		if should_run_task(task):
			now = datetime.now()
			logging.info("Running task {} at time {}".format(task,now))

			task_run = TaskRun(task.identifier, now)
			Session.persist(task_run)
			task.run()

			now = datetime.now()
			logging.info("Task {} completed at time {}".format(task.identifier,now))
			task_run.end_time = now

'''
A task should run if
1. It is non-recurring and hasn't been run
2. It is recurring and its schedule is "matched"
3. AND its dependencies have been met, if any
'''
def should_run_task(task):

	return (should_run_per_schedule(task) 
		and should_run_per_dependencies(task))

def should_run_per_schedule(task):
	
	'''
	Tasks that are not recurring should only be run once
	we'll check if they're in our "db". in reality we'd
	need something smarter if we didn't want to rely on
	history being wiped all the time
	'''
	if not task.recurring:
		task = Session.find_last_by_id(task.identifier)
		return not task

	#else recurring
	if time.matches_schedule(task.schedule):
		return True

'''
Figuring out exactly when a dependency has been met
requires some judgment calls. when the task is recurring,
do we look at the last run of the upstream task? how
do we know we haven't done a downstream run for that run
already? What do we do if an upstream task never finishes
before we schedule another downstream task?

Punting on some of these complexities.
'''
def should_run_per_dependencies(task):

	if not task.dependencies:
		return True

	#for now assume that we run downstream
	#only if the last upstream Run has an end_time
	satisfied = True
	for dependency in task.dependencies:
		task_run = Session.find_last_by_id(dependency)
		if not task_run or task_run.end_time is None:
			satisfied = False

	return satisfied
