import json,glob,re,sys,unicodedata
a=json.load(open("arts.json"))
def norm(s): return " ".join(s.split()).lower()
qs=[];bad=0;topic=None;topics={}
for f in sorted(glob.glob("q/*.txt")):
    for ln,l in enumerate(open(f,encoding="utf-8"),1):
        l=l.strip()
        if not l: continue
        if l.startswith("#"): topic=l[1:];topics.setdefault(topic,0);continue
        p=l.split("|")
        if len(p)!=8: print("FORMATO",f,ln,len(p));bad+=1;continue
        law,art,q,c,w1,w2,w3,cita=p
        t=a[law].get(art)
        if not t or norm(cita) not in norm(t["texto"]): print("CITA",f,ln,law,art,cita[:60]);bad+=1;continue
        if len({c,w1,w2,w3})<4: print("DUP",f,ln);bad+=1
        qs.append(dict(topic=topic,law=law,art=art,q=q,opts=[c,w1,w2,w3],cita=cita));topics[topic]+=1
print(len(qs),"ok;",bad,"errores");print(topics)
json.dump(qs,open("questions.json","w",encoding="utf-8"),ensure_ascii=False)
