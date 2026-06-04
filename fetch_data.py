import json
import datetime

raw = json.load(open('raw.json'))

for i, d in enumerate(raw['devices']):
    print(i, d.get('name'), d.get('serial'))
    for j, c in enumerate(d['channel']):
        print(' ch' + str(j), c.get('name'), c.get('value'), c.get('unit'))

dev = raw['devices'][0]
temp = float(dev['channel'][0]['value'])
hum = float(dev['channel'][1]['value'])

try:
    existing = json.load(open('data.json'))
    history = existing.get('history', [])
except:
    history = []

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
history.append({'time': now.strftime('%H:%M'), 'temp': temp, 'hum': hum})
history = history[-24:]

out = {
    'temperature': temp,
    'humidity': hum,
    'set_temperature': 28,
    'updated_at': now.isoformat(),
    'history': history
}

json.dump(out, open('data.json', 'w'), ensure_ascii=False, indent=2)
print('Done', temp, hum)
