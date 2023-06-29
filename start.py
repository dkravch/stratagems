import random

from aiohttp import web
import asyncio
from contextlib import suppress
from base import Strategems


class Periodic:

    def __init__(self, base_delay, random_delay):
        self.strategems = Strategems()
        self.actual_strategem = self.strategems.get_random_strategem()
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
            self.actual_strategem = self.strategems.get_random_strategem()
            print(self.actual_strategem)
            print('---')


class StrategemApplication:

    periodic = None

    async def app_factory(self):
        self.periodic = Periodic(base_delay=3, random_delay=3)
        print('Start')
        await self.periodic.start()
        app = web.Application()
        app.add_routes([web.get('/', self.current_strategem)])
        return app

    async def current_strategem(self, request):
        return web.Response(text=f"{self.periodic.actual_strategem['name']}")

    def __init__(self):
        web.run_app(self.app_factory(), port=8999)


StrategemApplication()
