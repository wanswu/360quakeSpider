import json

with open('bj.json', 'r',encoding='utf8') as f:
 data = f.read()
 data = json.loads(data)
for i in data:
 if 'hik' in i['cms']:
  print(i['url'])
