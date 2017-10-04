import importlib
import logging

from collections import Counter

# load a class object given the name in the config
def load_task_class(task_definition, tasks_base):

	(task_module_name, task_class_name) = task_definition['class'].split('.')
	full_task_module_name = tasks_base + '.' + task_module_name

	loaded_module = importlib.import_module(full_task_module_name)
	task_class = getattr(loaded_module, task_class_name)

	return task_class

# make sure we're defining our tasks in a sane fashion
def validate_config(config):
	#every task identifier should be unique
	ids_with_count = Counter(task['params']['identifier'] for task in config['tasks'])
	dupe_identifiers = [ident for ident, c in ids_with_count.items() if c > 1]

	if dupe_identifiers:
		raise ValueError('Multiple tasks with identifier(s) ' + str(dupe_identifiers))

	undefined_dependencies = []
	for task in config['tasks']:
		dependencies = task['params']['dependencies']
		if not dependencies:
			continue

		for d in dependencies:
			identifier = task['params']['identifier']
			if d not in ids_with_count:
				undefined_dependencies.append('Task: {}, Dependency: {}'.format(identifier, d))

	if undefined_dependencies:
		error = 'Some dependencies are undefined: {}'.format(undefined_dependencies)
		raise ValueError(error)


# convert a config into collection of concrete tasks
def instantiate_tasks(config):
	
	validate_config(config)

	tasks_base = config['tasks_base']

	tasks = {}
	for task_definition in config['tasks']:
		task_class = load_task_class(task_definition, tasks_base)
		task_instance = task_class(**task_definition['params'])

		tasks[task_instance.identifier] = task_instance
	
		logging.info('Instantiated task: ' + str(task_instance))

	return tasks
