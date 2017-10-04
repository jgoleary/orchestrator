import datetime

def matches_schedule(task_schedule):
	now = datetime.datetime.now()

	matches = True
	if 'on_second' in task_schedule:
		matches &= task_schedule['on_second']==now.second
	#TODO: on_minute, on_hour...

	return matches