import os

from base.application import StratagemApplication

port = int(os.environ.get('PORT', 8999))
periodic_task_base_delay = int(os.environ.get('BASE_DELAY', 3))
periodic_task_random_delay = int(os.environ.get('RANDOM_DELAY', 3))

StratagemApplication().run(port, periodic_task_base_delay, periodic_task_random_delay)
