"""Query GitHub API"""
from datetime import datetime
from urllib.request import urlopen
import json


def user_time(login):
    url = 'https://api.github.com/users/' + login
    resp = urlopen(url)
    reply = json.load(resp)
    # "2008-01-14T04:33:35Z", we trim the 'Z' with [:-1]
    ts = reply['created_at']
    created = datetime.fromisoformat(ts[:-1])
    return datetime.utcnow() - created


login = 'tebeka'
print(user_time(login))
