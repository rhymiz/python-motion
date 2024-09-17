# +
import os
from motion import Motion, MotionResponse

# Initialize the Motion client with the API token
motion = Motion(os.getenv("MOTION_API_TOKEN"))

# Fetch tasks
response = motion.tasks.list()
# -

dir(motion)

workspaces = motion.workspaces.list()

workspaces.json()


