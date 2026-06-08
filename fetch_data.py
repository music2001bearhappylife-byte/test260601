import json
import datetime
import urllib.request
import urllib.error
import os

api_key    = os.environ['API_KEY']
login_id   = os.environ['LOGIN_ID']
login_pass = os.environ['LOGIN_PASS']

body = json.dumps({
    'api-key':    api_key,
    'login-id':   login_id,
    'login-pass': login_pass
}).encode('utf-8')

req = urllib.request.Request(
    'https://api.webstorage.jp:443/v1/devices/current',
    data=body,
    headers={
        'Content-Type':           'application/json',
        'X-HTTP-Method-Override': 'GET'
    },
    method='POST'
)

try:
    with urllib.request.urlopen(req) as res:
        raw = json.loads(res.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print('HTTPエラー:', e.code)
    print('エラー詳細:', e.read().decode('utf-8'))
    exit(1)

print('=== APIの返答 ===')
print(json.dumps(raw, ensure_ascii=False, indent=2))
print('=== ここまで ===')

for i, d in enumerate(raw['devices']):
    print(i, d.get('name'), d.get('serial'))
    for j, c in enumerate(d['channel']):
        print(' ch' + str(j), c.get('name'), c.get('value'), c.get('unit'))

dev  = raw['devices'][0]
temp = float(dev['channel'][0]['value'])
hum  = float(dev['channel'][1]['value'])

try:
    existing = json.load(open('data.json'))
    history  = existing.get('history', [])
except:
    history = []

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
history.append({'time': now.strftime('%H:%M'), 'temp': temp, 'hum': hum})
history = history[-24:]

out = {
    'temperature':     temp,
    'humidity':        hum,
    'set_temperature': 28,
    'updated_at':      now.isoformat(),
    'history':         history
}

json.dump(out, open('data.json', 'w'), ensure_ascii=False, indent=2)
print('完了:', temp, hum)
