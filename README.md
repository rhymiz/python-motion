# Python Motion

A Python library for interfacing with the [Motion](https://wwww.usemotion.com)

🧪 This library is still in development and is not yet ready for production use.

### Installation

```bash
pip install python-motion
```

### Usage

```python
from motion import Motion

motion = Motion('your-api-key')

# Get Tasks
tasks = motion.tasks.list()
```


### Documentation

Library docs are a work in progress. For now, you can refer to the [official API documentation](https://docs.usemotion.com/) for more information.

Every resource has a `list`, `retrieve`, `create`, `update`, and `delete` method. 

```python
# List
tasks = motion.tasks.list()

# Retrieve
task = motion.tasks.retrieve('task-id')

# Create
task = motion.tasks.create({
    'name': 'Task Name',
    'description': 'Task Description'
})

# Update
task = motion.tasks.update('task-id', {
    'name': 'New Task Name'
})

# Delete
motion.tasks.delete('task-id')
```

#### Available Resources:
- [x] Tasks
- [x] Projects
- [x] Users
- [x] Workspaces
- [x] Comments
- [x] Schedule


### Roadmap
- [x] Initial implementation
- [ ] Named arguments for all methods
- [ ] Async support
- [ ] Convert responses to Pydantic models


## Using the Plugins

Installing the plugin:
```
pip install python_motion[todo]
```

Using the CLI:
```bash
$ todo 
Usage: todo [OPTIONS] COMMAND [ARGS]...

  todo - A tool to sync TODOs from text files with Motion API and export them.

Options:
  --debug  Enable debug logging.
  --help   Show this message and exit.

Commands:
  export  Export TODOs from files to a JSON file or Markdown table.
  sync    Sync TODOs from specified files with Motion API.
```

```bash
$ todo sync --help
Usage: todo sync [OPTIONS]

  Sync TODOs from specified files with Motion API.

Options:
  --dir DIRECTORY    Path to the directory containing files.  [required]
  --file-types TEXT  Comma-separated list of file extensions to scan for TODOs
                     (e.g., .tex,.py,.md).
  --api-key TEXT     API key for authentication (or set via MOTION_API_TOKEN
                     environment variable).
  --dry-run          Simulate the sync without making changes to the API.
  --export-json      Export TODOs to a JSON file.
  --json-path TEXT   Path to the output JSON file.
  --export-md        Export TODOs as a Markdown table.
  --md-path TEXT     Path to the output Markdown file.
  --help             Show this message and exit.
```
