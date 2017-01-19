import subprocess
import time
from matplotlib import pyplot as plt

def thread():
    p=subprocess.Popen('python task.py', shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return p

def run(n):
    t=time.time()
    res=[]
    pr=[]
    for i in range(n):
        p=thread()
        pr.append(p)
    while len(res)!=n:
        #time.sleep(0.01)
        for p in pr:
            out = p.communicate([0])[0]
            if out == '' and p.poll() != None:
                break
            if out != '':
                res.append(out)

    t1=time.time()

    return t1-t
        
x=range(1,17)
y=[]
for i in x:
    y.append(run(i))

plt.plot(x,y)
plt.grid()
plt.show()
