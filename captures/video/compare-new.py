import csv, json, statistics, collections
from pathlib import Path
summary={}; series={}; events={}
for name in ['5327','5328']:
 rows=list(csv.DictReader(open(f'captures/video/{name}-led-counts.csv')))
 frames=[(float(r['time']),[int(r[f'L{i}']) for i in range(10)]) for r in rows]
 stable=[(t,c) for t,c in frames if t>=10]
 bits=[tuple(int(max(c[i*2:i*2+2])>60) for i in range(5)) for t,c in stable]
 series[name]=bits
 pair_mismatch=[sum((c[2*i]>60)!=(c[2*i+1]>60) for t,c in stable)/len(stable) for i in range(5)]
 # Segment lit bursts separated by at least one dim frame; ignore incomplete/short bursts.
 bursts=[];current=[]
 for (t,c),b in zip(stable,bits):
  if any(b):current.append((t,c,b))
  elif current:bursts.append(current);current=[]
 ev=[]
 for q in bursts:
  if len(q)<5:continue
  mask=collections.Counter(b for t,c,b in q).most_common(1)[0][0]
  means=[sum(c[2*i]+c[2*i+1] for t,c,b in q)/len(q) for i in range(5)]
  dominant=max(range(5),key=lambda i:means[i])
  ev.append(dict(t=q[0][0],duration=q[-1][0]-q[0][0]+1/30,mask=mask,dominant=dominant))
 events[name]=ev
 masks=collections.Counter(''.join(map(str,b)) for b in bits if any(b))
 nonadj=0
 for b in bits:
  ids=[i for i,x in enumerate(b) if x]
  if len(ids)>2 or (len(ids)==2 and (ids[0]-ids[1])%5 not in [1,4]):nonadj+=1
 moves=[(v['dominant']-u['dominant'])%5 for u,v in zip(ev,ev[1:])]
 seq=[e['dominant'] for e in ev]
 repeat=[]
 for lag in range(1,min(65,len(seq)//2)):
  repeat.append((sum(x==y for x,y in zip(seq[:-lag],seq[lag:]))/(len(seq)-lag),lag))
 summary[name]=dict(frames=len(frames),stable_frames=len(stable),pair_mismatch=pair_mismatch,masks=masks,nonadjacent_or_more_than_two_frames=nonadj,events=len(ev),median_on=statistics.median(e['duration'] for e in ev),moves=collections.Counter(moves),best_event_repetition=sorted(repeat,reverse=True)[:3])
 Path(f'captures/video/{name}-events.json').write_text(json.dumps(ev,indent=2))
 print(name,json.dumps(summary[name],indent=2))
# Fine-time comparison; require at least 25 sec overlap, excluding common dim frames.
x,y=series['5327'],series['5328'];matches=[]
for lag in range(-600,601):
 start=max(0,-lag);ystart=max(0,lag);n=min(len(x)-start,len(y)-ystart)
 if n<750:continue
 pairs=list(zip(x[start:start+n],y[ystart:ystart+n]))
 active=[(a,b) for a,b in pairs if any(a) or any(b)]
 matches.append((sum(a==b for a,b in active)/len(active),lag/30,n))
summary['cross_video_best_active_mask_matches']=sorted(matches,reverse=True)[:5]
# Longest identical consecutive dominant-group sequence.
a=[e['dominant'] for e in events['5327']];b=[e['dominant'] for e in events['5328']]
prev=[0]*(len(b)+1);best=(0,0,0)
for i,xx in enumerate(a):
 cur=[0]*(len(b)+1)
 for j,yy in enumerate(b):
  if xx==yy:
   cur[j+1]=prev[j]+1
   if cur[j+1]>best[0]:best=(cur[j+1],i-cur[j+1]+1,j-cur[j+1]+1)
 prev=cur
summary['longest_shared_dominant_sequence']=dict(length=best[0],start_5327=best[1],start_5328=best[2],sequence=a[best[1]:best[1]+best[0]])
print('Comparison',json.dumps({k:v for k,v in summary.items() if k not in ['5327','5328']},indent=2))
Path('captures/video/new-comparison.json').write_text(json.dumps(summary,indent=2))
