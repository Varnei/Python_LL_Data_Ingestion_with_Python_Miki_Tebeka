import atexit
from pathlib import Path
from subprocess import PIPE, Popen
from time import monotonic, sleep
# from datetime import datetime
from random import seed, sample, randint

from neo4j import GraphDatabase
from neobolt.exceptions import ServiceUnavailable


here = Path(__file__).absolute().parent
csv_file = here / 'food.csv.bz2'

ports = [7474, 7687]

cmd = [
    'docker', 'run',
    '--rm', '--name', 'neo4j-demo',
    '--env', 'NEO4J_AUTH=none',
]
for port in ports:
    cmd.extend(['-p', f'{port}:{port}'])
cmd.append('neo4j')

proc = Popen(cmd, stdout=PIPE)
atexit.register(proc.kill)


driver = None
start = monotonic()
while monotonic() - start < 60:
    try:
        driver = GraphDatabase.driver('bolt://localhost')
        break
    except (OSError, ServiceUnavailable):
        sleep(0.1)

if driver is None:
    raise SystemExit('error: neo4j not up')


print('populating database...')
names = {
    'bugs': 'Bugs Bunny',
    'daffy': 'Daffy Duck',
    'porky': 'Porky Pig',
    'elmer': 'Elmer Fudd',
    'marvin': 'Marvin the Martian',
    'pepe': 'Pepe le Pew',
    'rr': 'Road Runner',
    'coyote': 'Wile E. Coyote'
}

seed('looney')
users = sorted(names)
graph = []
for user in users:
    count = randint(1, len(users)-1)
    following = sample([u for u in users if u != user], count)
    graph.append((user, following))


stmt = 'CREATE (a:User {login: $login, name: $name})'
db = driver.session()
for login, name in names.items():
    db.run(stmt, login=login, name=name)


stmt = '''
MATCH (a:User),(b:User)
WHERE a.login = $login AND b.login = $followed
CREATE (a)-[r:FOLLOWS]->(b)
RETURN type(r)
'''
for login, following in graph:
    for followed in following:
        db.run(stmt, login=login, followed=followed)


nusers = len(names)
nrelations = sum(len(v) for _, v in graph)
print(f'loaded {nusers} users with {nrelations} relations')

print(f'neo4j ready on ports {ports}, hit CTRL-C to quit')
try:
    proc.wait()
except KeyboardInterrupt:
    pass
print('\nkthxbai ☺')
