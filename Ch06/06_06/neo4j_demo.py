"""Working with neo4j"""
from neo4j import GraphDatabase

driver = GraphDatabase.driver('bolt://localhost')
db = driver.session()

# Who is daffy following?
login = 'daffy'

# Get name
name_query = '''
MATCH (a:User)
WHERE a.login = $login
RETURN a.name
'''

result = db.run(name_query, login=login)
name = result.value()[0]
print(f'name: {name}')

following_query = '''
MATCH (a:User)-[r:FOLLOWS]->(b:User)
WHERE a.login = $login
RETURN b
ORDER BY b.name
'''

res = db.run(following_query, login=login)
following = res.value()
print(f'{name} follows {len(following)} users')
for node in following:
    name, login = node['name'], node['login']
    print(f'- {name} ({login})')
