from pathlib import Path
import asyncio

from aiohttp import web
import aiohttp_jinja2
import jinja2


async def get_ps():

    create = asyncio.create_subprocess_exec('ps', '-auxf', stdout=asyncio.subprocess.PIPE)
    proc = await create

    data = await proc.stdout.read()
    text = data.decode('ascii')

    await proc.wait()
    return text


@aiohttp_jinja2.template('index.jinja')
async def handle(request):
    with open('/proc/cpuinfo') as f:
        return {
            'cpuinfo': f.read(),
            'psauxf': await get_ps()
        }


app = web.Application()

templates = Path(__file__).parent / 'templates'
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(templates.absolute())))

app.router.add_route('GET', '/', handle)
