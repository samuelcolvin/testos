from pathlib import Path

from aiohttp import web
import aiohttp_jinja2
import jinja2


@aiohttp_jinja2.template('index.jinja')
async def handle(request):
    with open('/proc/cpuinfo') as f:
        output = f.read()
    return {'output': output}


app = web.Application()

templates = Path(__file__).parent / 'templates'
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(templates.absolute())))

app.router.add_route('GET', '/', handle)
