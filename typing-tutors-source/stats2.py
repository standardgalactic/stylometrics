import json
exec(open('gen.py').read().split("res={")[0])
big=[w.strip() for w in open('words_alpha.txt') if w.strip()]
tot=sum(1/(r+1) for r in range(len(cands)))
def st(Kl,Nl):
    ad=[(r,w) for r,w in enumerate(cands) if set(w)<=Kl]
    nw=[w for r,w in ad if set(w)&Nl]
    cov=100*sum(1/(r+1) for r,w in ad)/tot
    b=sum(1 for w in big if set(w)<=Kl)
    return len(ad),len(nw),cov,b,[w for r,w in ad][:12]
K=set();rows=[]
for i,n in enumerate(order,1):
    K|=set(n)
    Kq=set(c for c in K if c.isalpha()); Nq=set(c for c in n if c.isalpha())
    Kd=set(q2d[c] for c in K if q2d[c].isalpha()); Nd=set(q2d[c] for c in n if q2d[c].isalpha())
    rows.append((i,st(Kq,Nq),st(Kd,Nd)))
json.dump(rows,open('rows.json','w'))
for r in rows: print(r[0],r[1][:4],r[2][:4])
print(rows[0][1][4]);print(rows[0][2][4]);print(len(cands))
