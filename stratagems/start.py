import random
import os

from aiohttp import web
import asyncio
import jinja2
import aiohttp_jinja2

from contextlib import suppress

from base.base import Stratagems

########################################################################################################################


class Periodic:

    def __init__(self, base_delay, random_delay):
        self.stratagems = Stratagems('./data/36.md')
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

    periodic = None

    async def app_factory(self):

        self.periodic = Periodic(base_delay=3, random_delay=3)
        print('Start')
        await self.periodic.start()

        app = web.Application()
        app.add_routes([web.get('/', self.current_stratagem)])

        aiohttp_jinja2.setup(app,
                             loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(),
                                                                         "templates")))

        return app

    async def current_stratagem(self, request):
        context = {
            'name': self.periodic.actual_stratagem['name'],
            'type': self.periodic.actual_stratagem['chapter'],
            'content': self.periodic.actual_stratagem['content'],

        }

        response = aiohttp_jinja2.render_template("stratagems.tpl",
                                                  request,
                                                  context=context)

        return response

    def __init__(self):
        web.run_app(self.app_factory(), port=8999)


StratagemApplication()
