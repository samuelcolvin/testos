from pathlib import Path
import asyncio

from aiohttp import web
import aiohttp_jinja2
import jinja2


async def exec_command(*command):

    create = asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE)
    proc = await create

    data = await proc.stdout.read()
    text = data.decode('ascii')

    await proc.wait()
    return text


@aiohttp_jinja2.template('index.jinja')
async def handle(request):
    with open('/proc/cpuinfo') as f:
        return {
            'info': [
                ('uname -a', await exec_command('uname', '-a')),
                ('/proc/cpuinfo', f.read()),
                ('ps -auxf', await exec_command('ps', '-auxf')),
            ]
        }


app = web.Application()

templates = Path(__file__).parent / 'templates'
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(str(templates.absolute())))

app.router.add_route('GET', '/', handle)
