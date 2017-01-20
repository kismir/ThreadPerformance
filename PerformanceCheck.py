import subprocess
import time
from matplotlib import pyplot as plt

########## SUBPROCESSING PART

def push_task():
    p=subprocess.Popen('python task.py', shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return p

def run_sub(n):
    t=time.time()
    res=[]
    pr=[]
    for i in range(n):
        p=push_task()
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

def system_subprocess_test():
    x=range(1,17)
    y=[]
    for i in x:
        y.append(run_sub(i))

    plt.plot(x,y)
    plt.grid()
    plt.show()

############# THREADING PART
from queue import Queue
from threading import Thread

def threading_task(out):
    t=time.time()
    k=0
    for i in range(10000000):
        k=k+1
    t1=time.time()
    #print(t1-t)
    out.put(t1-t)

def run_thread(n):
    t=time.time()
    q = Queue()
    tp=[]
    for i in range(1,n+1):
        t_proc = Thread(target=threading_task, args=(q,))
        t_proc.daemon=True
        t_proc.start()
    a=[]
    while len(a)!=n:
        z=q.get()
        if z!=None:
            a.append(z)

    t1=time.time()
    
    return (t1-t)

def system_thread_test():
    x=range(1,17)
    y=[]
    for i in x:
        y.append(run_thread(i))

    plt.plot(x,y)
    plt.grid()
    plt.show()
    
system_subprocess_test()
system_thread_test()

# multiprocessing
