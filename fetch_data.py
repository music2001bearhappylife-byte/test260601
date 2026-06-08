import json
import datetime
import urllib.request
import urllib.error
import os

api_key    = os.environ['API_KEY']
login_id   = os.environ['LOGIN_ID']
login_pass = os.environ['LOGIN_PASS']

print('API_KEY長さ:', len(api_key))
print('LOGIN_ID:', login_id)
print('LOGIN_PASS長さ:', len(login_pass))

body = json.dumps({
    'api-key':    api_key,
    'login-id':   login_id,
    'login-pass': login_pass
}).encode('utf-8')

print('送信JSON:', body.decode('utf-8'))

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
    print('=== APIの返答 ===')
    print(json.dumps(raw, ensure_ascii=False, indent=2))
except urllib.error.HTTPError as e:
    print('HTTPエラー:', e.code)
    print('エラー詳細:', e.read().decode('utf-8'))
