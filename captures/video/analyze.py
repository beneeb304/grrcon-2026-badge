from PIL import Image
from pathlib import Path
import numpy as np,json
for name in ['5316','5318']:
 records=[]
 for p in sorted(Path('captures/video').glob('dense-'+name+'-*.png')):
  sec=int(p.stem.split('-')[-1])/100
  if sec<10:continue
  a=np.asarray(Image.open(p).convert('RGB')).astype(float)
  y,x=np.indices(a.shape[:2]);r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
  board=(g>r*1.2)&(g>b*1.04)&(g>30)&(x>380)&(y<325)
  yy,xx=np.where(board)
  if len(xx)<3000:continue
  xmin,xmax=np.percentile(xx,[1,99]); ymin,ymax=np.percentile(yy,[1,99])
  cx=(xmin+xmax)/2;cy=(ymin+ymax)/2;rx=(xmax-xmin)/2;ry=(ymax-ymin)/2
  nx=(x-cx)/rx;ny=(y-cy)/ry
  rad=(nx*nx+ny*ny)**.5;angle=np.degrees(np.arctan2(ny,nx))
  group=((angle+145)%360//72).astype(int)
  lit=(g>160)&(g-r>45)&(g-b>20)&(rad>.82)&(rad<1.18)&(x>380)&(y<325)
  counts=[int(np.sum(lit&(group==i))) for i in range(5)]
  bits=[int(n>12) for n in counts]
  records.append({'t':sec,'bits':bits,'counts':counts,'center':[round(cx,1),round(cy,1)]})
 Path('captures/video/'+name+'-activity.json').write_text(json.dumps(records))
 print(name,'frames',len(records),'unique bright-group masks',len(set(tuple(q['bits']) for q in records)))
 print('sample',[(q['t'],''.join(map(str,q['bits']))) for q in records[:40]])
 arr=np.array([q['bits'] for q in records]);active=arr.sum(1)>0
 results=[]
 for lag in range(2,min(100,len(arr)//2)):
  valid=active[:-lag]|active[lag:]
  same=np.all(arr[:-lag]==arr[lag:],axis=1)
  results.append((round(float(np.mean(same[valid])),3),lag*.25))
 print('best within-video lag matches',sorted(results,reverse=True)[:5])
