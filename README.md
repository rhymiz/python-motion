# Python Motion

A Python library for interfacing with the [Motion](https://wwww.usemotion.com)

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


### Roadmap
- [x] Initial implementation
- [ ] Named arguments for all methods
- [ ] Async support
- [ ] Convert responses to Pydantic models