import re, json
words=open('text.txt').read().split()
s=[float(l.split()[1]) for l in open('sil.txt')]
kinds=[l.split(':')[0] for l in open('sil.txt')]
# build silence intervals
sil=[];i=0
while i<len(s):
    if kinds[i]=='silence_start' and i+1<len(s): sil.append((s[i],s[i+1])); i+=2
    else: i+=1
END=float(open('dur.txt').read())
# speech start
first_speech=0.0
if sil and sil[0][0]<0.05: first_speech=sil[0][1]; sil=sil[1:]
def vow(w): return max(1,len(re.findall(r'[aeiouáéíóúâêôãõà]+',w.lower())))
wt=[vow(w)+ (0.6 if re.search(r'[,.?!:]"?$',w) else 0) for w in words]
# boundary strength after each word
def bstr(w):
    if re.search(r'[.?!]"?$',w): return 3
    if w.endswith(':'): return 2
    if w.endswith(','): return 1
    return 0
B=[bstr(w) for w in words]
# DP: assign pauses (in order) to word boundaries (word index k means pause after word k), each pause assigned or skipped.
# segments of speech between consecutive assigned pauses must have rate close to global rate.
speech_total=END-first_speech-sum(b-a for a,b in sil)
rate=sum(wt)/speech_total
import math
cum=[0]
for x in wt: cum.append(cum[-1]+x)
P=len(sil); N=len(words)
# candidate boundaries: indices with B>0, plus last
cands=[k for k in range(N-1) if B[k]>0]
INF=1e18
# dp over pauses with state = boundary chosen; allow skipping pauses (cost by pause len) and skipping punctuation (cost by strength)
from functools import lru_cache
import sys
sys.setrecursionlimit(10000)
times_start=[first_speech]+[b for a,b in sil]   # speech segment starts
times_end=[a for a,b in sil]+[END]
# simplified: choose subset of pauses mapped to subset of candidate boundaries monotonically
# dp[j][c] = min cost having mapped pause j to cand c
dp={}
def seg_cost(w0,w1,t0,t1):
    exp=(cum[w1]-cum[w0])/rate
    d=t1-t0
    return ((d-exp)/max(exp,0.5))**2*4
# include skipped pauses inside a segment: their duration subtract from speech
best={}
# state: (last pause idx assigned or -1, last word boundary idx) -> cost; speech time accounting with skipped pauses
import itertools
prevs={(-1,-1):(0.0,None)}
order=[]
for j in range(P):
    a,b=sil[j]
    plen=b-a
    for c in cands:
        bestv=INF;arg=None
        for (pj,pc),(v,_) in prevs.items():
            if pc>=c or pj>=j: continue
            w0=pc+1; w1=c+1
            t0=first_speech if pj<0 else sil[pj][1]
            t1=a
            skipped=sum(sil[k][1]-sil[k][0] for k in range(pj+1,j))
            # skipped pauses count as speech-time removal
            cost=v+seg_cost(w0,w1,t0,t1-skipped)
            cost+=sum(min(3,(sil[k][1]-sil[k][0])*6) for k in range(pj+1,j))  # penalty skipping pauses
            cost+=sum({1:0.6,2:1.5,3:3}[B[k]] for k in range(pc+1,c) if B[k]>0)  # penalty skipping punct
            cost-= {1:0.2,2:0.4,3:0.8}[B[c]]*min(1,plen*2)
            if cost<bestv: bestv=cost;arg=(pj,pc)
        if arg is not None: prevs[(j,c)]=(bestv,arg)
# terminate
bestv=INF;fin=None
for (pj,pc),(v,_) in prevs.items():
    if pj<0: continue
    skipped=sum(sil[k][1]-sil[k][0] for k in range(pj+1,P))
    cost=v+seg_cost(pc+1,N,sil[pj][1],END-0.2-skipped)+sum(min(3,(sil[k][1]-sil[k][0])*6) for k in range(pj+1,P))
    cost+=sum({1:0.6,2:1.5,3:3}[B[k]] for k in range(pc+1,N-1) if B[k]>0)
    if cost<bestv: bestv=cost;fin=(pj,pc)
anch=[];st=fin
while st and st!=(-1,-1):
    anch.append(st); st=prevs[st][1]
anch=anch[::-1]
# build word times: within segment between anchors, distribute by weight over speech time excluding skipped pauses
res=[None]*N
bounds=[(-1,-1)]+anch+[(P,N-1)]
for (pj,pc),(nj,nc) in zip(bounds,bounds[1:]):
    t0=first_speech if pj<0 else sil[pj][1]
    t1=END-0.2 if nj>=P else sil[nj][0]
    inner=[sil[k] for k in range(pj+1,min(nj,P))]
    w0,w1=pc+1,nc+1
    tot=cum[w1]-cum[w0]
    spd=(t1-t0)-sum(b-a for a,b in inner)
    def mapt(x):  # x in speech seconds from t0
        t=t0
        for a,b in inner:
            if t0+x+ (t-t0 - 0) <0: pass
        # walk
        rem=x;t=t0
        for a,b in inner:
            if t+rem<=a: return t+rem
            rem-= (a-t); t=b
        return t+rem
    acc=0
    for k in range(w0,w1):
        st_=mapt(acc/tot*spd); acc+=wt[k]; en=mapt(acc/tot*spd)
        res[k]=(round(st_,3),round(en,3))
out=[{"w":w,"s":r[0],"e":r[1]} for w,r in zip(words,res)]
json.dump(out,open('words.json','w'),ensure_ascii=False,indent=0)
for a in anch: print(round(sil[a[0]][0],2), words[a[1]])
