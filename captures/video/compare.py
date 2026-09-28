from PIL import Image
from pathlib import Path
import numpy as np,json
positions={
 '5316':[(595,45),(672,18),(748,36),(789,96),(753,214),(704,261),(640,280),(580,269),(530,215),(530,128)],
 '5318':[(481,40),(556,20),(626,43),(666,99),(643,222),(598,264),(534,281),(475,266),(424,205),(423,114)]}
allseq={}
for name in ['5316','5318']:
 tracking=json.load(open('captures/video/'+name+'-activity.json'));track={q['t']:q['center'] for q in tracking}
 ref=track[20.0 if name=='5316' else 24.0];seq=[]
 for p in sorted(Path('captures/video').glob('dense-'+name+'-*.png')):
  t=int(p.stem.split('-')[-1])/100
  if t<12:continue
  a=np.asarray(Image.open(p).convert('RGB')).astype(float);r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
  cy,cx=0,0
  shift=np.array(track[t])-ref;active=[];counts=[]
  for x,y in positions[name]:
   x,y=np.rint(np.array([x,y])+shift).astype(int)
   rr=r[max(0,y-10):y+11,max(0,x-10):x+11];gg=g[max(0,y-10):y+11,max(0,x-10):x+11];bb=b[max(0,y-10):y+11,max(0,x-10):x+11]
   n=int(np.sum((gg>170)&(gg-rr>45)&(gg-bb>15)));counts.append(n);active.append(n>15)
  bits=[int(active[2*i] or active[2*i+1]) for i in range(5)]
  seq.append({'t':t,'bits':bits,'counts':counts})
 Path('captures/video/'+name+'-groups.json').write_text(json.dumps(seq))
 print(name,'sample',[(q['t'],''.join(map(str,q['bits']))) for q in seq[:32]])
 arr=np.array([q['bits'] for q in seq]);results=[]
 for lag in range(2,min(100,len(arr)//2)):
  valid=(arr[:-lag].sum(1)>0)|(arr[lag:].sum(1)>0)
  same=np.all(arr[:-lag]==arr[lag:],axis=1)
  results.append((round(float(np.mean(same[valid])),3),lag*.25))
 print('within-video lag matches',sorted(results,reverse=True)[:4]);allseq[name]=arr
x,y=allseq['5316'],allseq['5318'];res=[]
for lag in range(-80,81):
 start=max(0,-lag);ystart=max(0,lag);n=min(len(x)-start,len(y)-ystart)
 if n<80:continue
 xx=x[start:start+n];yy=y[ystart:ystart+n];valid=(xx.sum(1)>0)|(yy.sum(1)>0)
 res.append((round(float(np.mean(np.all(xx==yy,axis=1)[valid])),3),lag*.25,n))
print('between videos matches',sorted(res,reverse=True)[:5])
