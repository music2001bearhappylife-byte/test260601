import json
import datetime

# raw.jsonを読み込む
with open('raw.json') as f:
    raw = json.load(f)

# 全機器の名前を表示（デバッグ用）
print("=== 取得できた機器一覧 ===")
for i, dev in enumerate(raw['devices']):
    print(f"[{i}] 機器名: {dev.get('name', '不明')} / シリアル: {dev.get('serial', '不明')}")
    for j, ch in enumerate(dev['channel']):
        print(f"    ch{j}: {ch.get('name','不明')} = {ch.get('value','--')} {ch.get('unit','')}")

# ★ここを機器名に合わせて変更する★
TARGET_DEVICE_NAME = "ここに機器名を入れる"

# 機器名で検索
target = None
for dev in raw['devices']:
    if dev.get('name') == TARGET_DEVICE_NAME:
        target = dev
        break

# 見つからなければ最初の機器を使う
if target is None:
    print(f"警告: '{TARGET_DEVICE_NAME}' が見つからないため最初の機器を使用します")
    target = raw['devices'][0]

channels = target['channel']
temp = float(channels[0]['value'])
hum  = float(channels[1]['value'])

# 既存のhistoryを読み込んで追記
try:
    with open('data.json') as f:
        existing = json.load(f)
    history = existing.get('history', [])
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

with open('data.json', 'w') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(f"完了: 温度={temp} 湿度={hum}")
