import re,json,sys
out={}
for law,f in [("CE","boe/BOE-A-1978-31229.md"),("L39","boe/BOE-A-2015-10565.md"),("L40","boe/BOE-A-2015-10566.md")]:
    txt=open(f,encoding="utf-8").read()
    parts=re.split(r'^##### (Artículo \d+(?: bis)?)\.?[ \t]*(.*)$',txt,flags=re.M)
    arts={}
    for i in range(1,len(parts),3):
        num=re.search(r'\d+(?: bis)?',parts[i]).group(0)
        body=parts[i+2].split("\n#")[0].replace("\n---","").strip()
        if num not in arts: arts[num]={"titulo":parts[i+1].strip(),"texto":body}
    out[law]=arts
json.dump(out,open("build/arts.json","w",encoding="utf-8"),ensure_ascii=False)
for k,v in out.items(): print(k,len(v))
