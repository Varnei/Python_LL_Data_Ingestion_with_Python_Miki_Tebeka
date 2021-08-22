import atexit
import json
from pathlib import Path
from subprocess import PIPE, Popen
from time import monotonic, sleep

from redis import Redis, RedisError

here = Path(__file__).absolute().parent
data_file = here / 'commerce.jl'

port = 6379

cmd = [
    'docker', 'run',
    '--rm', '-p', f'{port}:{port}',
    '--name', 'redis-demo',
    'redis:alpine',
]

proc = Popen(cmd, stdout=PIPE)
atexit.register(proc.kill)

up = False
start = monotonic()
while monotonic() - start < 60:
    conn = Redis()
    try:
        if conn.ping():
            up = True
            break
    except RedisError:
        sleep(0.1)

if not up:
    raise SystemExit('error: redis not up')

print('populating database...')
with open(data_file) as fp:
    for line in fp:
        obj = json.loads(line)
        key = f'tid:{obj["id"]}'
        conn.set(key, line[:-1])


print(f'redis ready on port {port}, hit CTRL-C to quit')
try:
    proc.wait()
except KeyboardInterrupt:
    pass
print('\nkthxbai ☺')
