import requests
from pprint import pprint

res = requests.get('https://dt.miet.ru/ppo_it_final', headers={'X-Auth-Token': 'dzxylhiz'})

pprint(res.json())
