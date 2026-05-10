"""Push new article files + images to GitHub via REST API"""
import base64, json, os, sys, time, urllib.request, urllib.error

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\15645\Desktop\githubToken.txt', 'r') as f:
    token = f.read().strip()

owner, repo, branch = 'auxwy1328', 'chromebest', 'master'
api = f'https://api.github.com/repos/{owner}/{repo}/contents'
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'Mozilla/5.0'
}

files_to_push = [
    'content/tips/chrome-clear-cache.md',
    'content/tips/chrome-extensions-not-working.md',
    'static/images/tips/chrome-clear-cache/cover.jpg',
    'static/images/tips/chrome-clear-cache/body1.jpg',
    'static/images/tips/chrome-extensions-not-working/cover.jpg',
    'static/images/tips/chrome-extensions-not-working/body1.jpg',
]

def get_sha(path):
    url = f'{api}/{path}?ref={branch}'
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        return data.get('sha')
    except:
        return None

def push_file(path):
    local = os.path.join(r'C:\Projects\chromebest', path.replace('/', os.sep))
    if not os.path.exists(local):
        print(f'  SKIP (not found): {path}')
        return False
    
    with open(local, 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    
    sha = get_sha(path)
    payload = {
        'message': f'Add {os.path.basename(path)}',
        'content': content,
        'branch': branch,
    }
    if sha:
        payload['sha'] = sha
    
    url = f'{api}/{path}'
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method='PUT')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
        print(f'  OK: {path}')
        return True
    except urllib.error.HTTPError as e:
        print(f'  FAIL ({e.code}): {path}')
        return False

print(f'Pushing {len(files_to_push)} files...')
success = 0
for f in files_to_push:
    if push_file(f):
        success += 1
    time.sleep(1)

print(f'\nDone: {success}/{len(files_to_push)} files pushed')
