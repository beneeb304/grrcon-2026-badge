import os,termios,select,time,json,sys
baud=int(sys.argv[1]); duration=int(sys.argv[2])
fd=os.open('/dev/cu.usbmodemflip_H1x1on1',os.O_RDWR|os.O_NOCTTY|os.O_NONBLOCK)
a=termios.tcgetattr(fd)
a[0]=0; a[1]=0; a[2]=termios.CLOCAL|termios.CREAD|termios.CS8; a[3]=0
a[4]=a[5]=getattr(termios,'B'+str(baud)); a[6][termios.VMIN]=0; a[6][termios.VTIME]=0
termios.tcsetattr(fd,termios.TCSANOW,a)
print('Listening at '+str(baud)+' baud',flush=True)
end=time.monotonic()+duration; total=0
with open('captures/uart-'+str(baud)+'.bin','ab') as out:
 while time.monotonic()<end:
  ready,_,_=select.select([fd],[],[],1)
  if ready:
   data=os.read(fd,4096)
   if data:
    out.write(data); out.flush(); total+=len(data)
    print(json.dumps({'bytes':len(data),'text':data.decode('utf-8','backslashreplace'),'hex':data.hex()}),flush=True)
os.close(fd)
print('Capture finished: '+str(total)+' bytes',flush=True)
