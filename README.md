# orchestrator
## A skeleton of a simple-minded task orchestration service

To launch, `cd` into the orchestrator directory and run

```
python3 orchestrator.py ../tests/test_config.yaml
```

This will launch the service based on the tasks defined in the `test_config.yaml` file. Upon startup, this config file will be read and tasks will be instantiated according to the task types and parameters specified therein. From then, an infinite loop will be started. Upon every step of this loop, the set of instantiated tasks will be examined and any that meet criteria to be run will have their `run()` method called. To exit, use `^C`.

A sample task configuration snippet follows:
```
- class: fetch_latest_file.FetchLatestFile
  params:
    identifier: tmp_watcher
    recurring: True
    schedule: 
      on_second: 5
    dependencies: null
    path: /tmp
```
The `class` attribute specifies the python class that stores the generic logic to be used for this task. The `params` dictionary specifies the parameters to be used to control the behavior of this specific task instance. The first 4 are common across all task instances. The last parameter is specific to the `FetchLatestFile` task. 

An example of how this might be utilized: Suppose you want to watch several different directories for incoming files. One task could be instantiated for each directory you need to watch, with a different `path` specified for each. Downstream processing of those arriving files could be effected by defining tasks that point back to the `identifier` of the appropriate upstream tasks in their `dependencies` lists.
