import json
Q="qwertyuiopasdfghjkl;zxcvbnm,./"
D="',.pyfgcrlaoeuidhtns;qjkxbmwvz"
q2d=dict(zip(Q,D))
order=["asdfjkl;","gh","eu","ro","ty","wi","nm","vb","c,","qp","x.","/","z"]
colhome={}
for cols,h in [("qaz","a"),("wsx","s"),("edc","d"),("rfvtgb","f"),("yhnujm","j"),("ik,","k"),("ol.","l"),("p;/",";")]:
    for c in cols: colhome[c]=h
black=set("las fla fl al ala ads ass lass sass alas dfa jak jag kaj ska sal dallas alaska texas mexico amazon zealand january august dvd hotels texas kansas alabama".split())
freq=[w.strip() for w in open('g10k.txt') if w.strip() and w.strip().isalpha()]
freq=[w for w in freq if len(w)>=3 or w in ('as','at','an','on','to','up','us','is','it','in','if','of','or','no','so','do','go','he','me','we','be','by','my','am','oh','ok','ad')]
cands=[w for w in freq if w not in black]
def chain(i,n,K):
    if i==1: return "asdf ;lkj"
    if i==2: return "asdfg ;lkjh"
    left=[c for c in n if c in "qwertasdfgzxcvb"]; right=[c for c in n if c not in "qwertasdfgzxcvb"]
    s=" ".join(colhome[c]+c+colhome[c] for c in left+right)
    return s
def caps(s,n):
    out=""
    for c in s:
        out+= c.upper() if (c in n and c.isalpha()) else c
    return out
def mapstr(s): return "".join(q2d.get(c,c) for c in s)
def capsmapped(s,n):
    # s in qwerty; new keys capitalised where mapped result is a letter
    out=""
    for c in s:
        m=q2d.get(c,c)
        out+= m.upper() if (c in n and m.isalpha()) else m
    return out
def pick(words,Kl,Nl,lo,hi,k):
    res=[w for w in words if set(w)<=Kl and set(w)&Nl and lo<=len(w)<=hi]
    return res[:k]
def phrase(words,Kl,Nl):
    w=[x for x in words if set(x)<=Kl and set(x)&Nl and 2<=len(x)<=4]
    return " ".join(w[:5])
def build(layout):
    K=set();out=[]
    for i,n in enumerate(order,1):
        K|=set(n)
        if layout=="q":
            Kl={c for c in K}; Nl={c for c in n}
            g1=chain(i,n,K); g2=caps(g1,n) if i>2 else g1+"a"
            # ex1/2 : old-key insertion
            if i==1: g2="asdfa ;lkj;"
            if i==2: g2="asdfgfa ;lkjhj;"
        else:
            Kl={q2d[c] for c in K}; Nl={q2d[c] for c in n}
            g1=mapstr(chain(i,n,K)); g2=capsmapped(chain(i,n,K),n) if i>2 else None
            if i==1: g2=mapstr("asdfa ;lkj;")
            if i==2: g2=mapstr("asdfgfa ;lkjhj;")
        g3=pick(cands,Kl,Nl,3,4,4); g4=pick(cands[10:] if False else cands,Kl,Nl,4,5,4)
        g5=pick(cands,Kl,Nl,6,9,4) or pick(cands,Kl,Nl,5,9,4); g6=phrase(cands,Kl,Nl)
        out.append(dict(i=i,new="".join(sorted(Nl)),g1=g1,g2=g2,g3=g3,g4=g4,g5=g5,g6=g6))
    return out
res={"q":build("q"),"d":build("d")}
json.dump(res,open('corpus.json','w'),indent=1)
for lay in "qd":
    print("=====",lay)
    for e in res[lay]:
        print(e['i'],e['new'],'|',e['g1'],'|',e['g2'],'|',e['g3'],e['g4'],e['g5'],'|',e['g6'])
