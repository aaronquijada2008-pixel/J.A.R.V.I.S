#!/usr/bin/env python3
import urllib.request,zipfile,io,sys,re
RUN_ID=31567211328
OWNER='aaronquijada2008-pixel'
REPO='J.A.R.V.I.S'
url=f'https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{RUN_ID}/logs'
print('Downloading',url)
resp=urllib.request.urlopen(url)
data=resp.read()
print('Downloaded',len(data),'bytes')
zf=zipfile.ZipFile(io.BytesIO(data))
files=zf.namelist()
print('Files in zip:',len(files))
# prefer files with job name
candidates=[f for f in files if 'build-windows' in f or 'Build EXE' in f or 'pyinstaller' in f or f.endswith('.txt')]
if not candidates:
    candidates=files
# search for error patterns
matches=[]
pat=re.compile(r'Traceback|ERROR|Exception|Error:|failed', re.IGNORECASE)
for f in candidates:
    try:
        txt=zf.read(f).decode(errors='ignore')
    except Exception:
        continue
    if pat.search(txt):
        matches.append((f,txt))
# select
if matches:
    best_file, out = matches[0]
    print('Found error patterns in:', best_file)
else:
    best_file = max(files, key=lambda x: zf.getinfo(x).file_size)
    out = zf.read(best_file).decode(errors='ignore')
    print('No explicit error patterns found; showing tail of largest file:', best_file)
lines = out.splitlines()
TAIL = 300
print('\n--- LAST %d LINES OF %s ---\n' % (TAIL, best_file))
print('\n'.join(lines[-TAIL:]))
