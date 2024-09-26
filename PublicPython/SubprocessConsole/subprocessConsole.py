import subprocess
a = 'ls /home/guit/Documents/tftp'
b = subprocess.run(a, stdout=subprocess.PIPE, shell=True) 
c = b.stdout.decode('utf-8') 
for i in c.split('\n'):
   print(i, 1)