from aiohttp import web
import asyncio
from contextlib import suppress


class Periodic:
    def __init__(self, func, time):
        self.func = func
        self.time = time
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
            await asyncio.sleep(self.time)
            self.func()


async def hello(request):

    return web.Response(text="Hello, world")


async def app_factory():
    p = Periodic(lambda: print('test'), 1)
    print('Start')
    await p.start()
    app = web.Application()
    app.add_routes([web.get('/', hello)])
    return app

web.run_app(app_factory(), port=8999)
