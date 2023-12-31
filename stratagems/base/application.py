import random
import os

from aiohttp import web
import asyncio
import jinja2
import aiohttp_jinja2

from contextlib import suppress

from base.data_structure import Stratagems

########################################################################################################################


class Periodic:

    def __init__(self, base_delay, random_delay):
        self.stratagems = Stratagems('./data/36.md')  # TODO Avoid hard-coding
        self.actual_stratagem = self.stratagems.get_random_stratagem()
        self.base_delay = base_delay
        self.random_delay = random_delay
        self.is_started = False
        self._task = None

    async def start(self):
        if not self.is_started:
            self.is_started = True
            # Start task to call func periodically:
            self._task = asyncio.ensure_future(self._run())

    async def stop(self):
        if self.is_started:
            self.is_started = False
            # Stop task and await it stopped:
            self._task.cancel()
            with suppress(asyncio.CancelledError):
                await self._task

    async def _run(self):
        while True:
            await asyncio.sleep(self.base_delay + random.randint(0, self.random_delay + 1))
            self.actual_stratagem = self.stratagems.get_random_stratagem()
            print(self.actual_stratagem)
            print('---')


########################################################################################################################


class StratagemApplication:

    periodic_task = None

    async def app_factory(self,
                          periodic_task_base_delay,
                          periodic_task_random_delay):

        self.periodic_task = Periodic(base_delay=periodic_task_base_delay,
                                      random_delay=periodic_task_random_delay)
        print('Start')
        await self.periodic_task.start()

        app = web.Application()
        app.add_routes([web.get('/', self.current_stratagem)])

        aiohttp_jinja2.setup(app,
                             loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(),
                                                                         "templates")))

        return app

    async def current_stratagem(self, request):
        context = {
            'name': self.periodic_task.actual_stratagem['name'],
            'type': self.periodic_task.actual_stratagem['chapter'],
            'content': self.periodic_task.actual_stratagem['content'],

        }

        response = aiohttp_jinja2.render_template("stratagems.tpl",
                                                  request,
                                                  context=context)

        return response

    def run(self, port=8999, periodic_task_base_delay=3, periodic_task_random_delay=3):
        web.run_app(self.app_factory(periodic_task_base_delay=periodic_task_base_delay,
                                     periodic_task_random_delay=periodic_task_random_delay),
                    port=port)  # TODO Parameterize port and periodic delay
