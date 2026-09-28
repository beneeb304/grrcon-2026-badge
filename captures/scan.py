import os,termios,select,time,json,datetime
rates=[9600,19200,38400,57600,115200,230400,4800,2400,1200,600,300]
fd=os.open('/dev/cu.usbmodemflip_H1x1on1',os.O_RDWR|os.O_NOCTTY|os.O_NONBLOCK)
run=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
summary=[]
try:
 for baud in rates:
  a=termios.tcgetattr(fd)
  a[0]=0;a[1]=0;a[2]=termios.CLOCAL|termios.CREAD|termios.CS8;a[3]=0
  a[4]=a[5]=getattr(termios,'B'+str(baud));a[6][termios.VMIN]=0;a[6][termios.VTIME]=0
  termios.tcsetattr(fd,termios.TCSANOW,a)
  termios.tcflush(fd,termios.TCIFLUSH)
  print('NOW '+str(baud)+' baud (10 seconds)',flush=True)
  end=time.monotonic()+10; data=bytearray()
  while time.monotonic()<end:
   ready,_,_=select.select([fd],[],[],min(1,max(0,end-time.monotonic())))
   if ready:
    chunk=os.read(fd,4096)
    if chunk:
     data.extend(chunk)
     print(json.dumps({'baud':baud,'hex':chunk.hex(),'text':chunk.decode('utf-8','backslashreplace')}),flush=True)
  with open('captures/scan-'+run+'-'+str(baud)+'.bin','wb') as f:f.write(data)
  summary.append({'baud':baud,'bytes':len(data),'hex':data.hex()})
finally:
 os.close(fd)
 with open('captures/scan-'+run+'-summary.json','w') as f:json.dump(summary,f,indent=2)
print(json.dumps(summary),flush=True)
