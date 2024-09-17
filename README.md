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


