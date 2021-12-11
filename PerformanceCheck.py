import time
from matplotlib import pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as tkr

import subprocess
from queue import Queue
from threading import Thread
from multiprocessing import Process, Pool
from multiprocessing import Queue as QUE
########## SUBPROCESSING PART

def func(x, pos):  # formatter function takes tick label and tick position
    s = str(x)
    ind = s.index('.')
    return s[:ind] + ',' + s[ind+1:]   # change dot to comma

def plt_stats():
    mpl.rcParams['font.family'] = 'fantasy'
    mpl.rcParams['font.fantasy'] = 'Arial'

    mpl.rc('xtick', labelsize=14) 
    mpl.rc('ytick', labelsize=14)

    plt.subplots_adjust(left=0.15, right=0.97, top=0.95, bottom=0.1)
    plt.grid(True)
    ax = plt.gca()
    y_format = tkr.FuncFormatter(func)  # make formatter
    ax.yaxis.set_major_formatter(y_format)
    #ax.xaxis.set_major_formatter(y_format)
    #ax.set_xticks(np.arange(0,11,1))
    ax.yaxis.set_label_coords(-0.1, 0.46)

def push_task():
    p=subprocess.Popen('python task.py', shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return p

def run_sub_readline(n):
    t=time.time()
    res=[]
    pr=[]
    for i in range(n):
        p=push_task()
        pr.append(p)
    while len(res)!=n:
        for p in pr:
            out=p.stdout.readline()
            if out!='':
                res.append((out,p.pid))

    t1=time.time()

    return t1-t

def run_sub_communicate(n):
    t=time.time()
    res=[]
    pr=[]
    for i in range(n):
        p=push_task()
        pr.append(p)
#    while len(res)!=n:
    for p in pr:
        out = p.communicate([0])[0]
        if out != '':
            res.append(out)

    t1=time.time()

    return t1-t

def system_subprocess_test():
    x=range(1,17)
    y=[]
    y1=[]
    for i in x:
        y.append(run_sub_readline(i))
        y1.append(run_sub_communicate(i))

    plt.figure(1)
    plt.plot(x,y,x,y1)
    plt.grid()
    plt.show(block=False)

    return ((x,y),(x,y1))

############# THREADING PART

def threading_task(out):
    t=time.time()
    k=0
    for i in range(10000000):
        k=k+1
    t1=time.time()
    out.put(t1-t)

def run_thread(n):
    t=time.time()
    q = Queue()
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
    
    return t1-t

def system_thread_test():
    x=range(1,17)
    y=[]
    for i in x:
        y.append(run_thread(i))

    plt.figure(2)
    plt.plot(x,y)
    plt.grid()
    plt.show(block=False)

    return (x,y)
    
############# MULTIPROCESSING

def multiprocessing_task_q(out):
    t=time.time()
    k=0
    for i in range(10000000):
        k=k+1
    t1=time.time()
    out.put(t1-t)

def multiprocessing_task(_):
    t=time.time()
    k=0
    for i in range(10000000):
        k=k+1
    t1=time.time()

    return t1-t

def run_multiprocess_process(n):
    t=time.time()
    q = QUE()
    tp=[]
    for i in range(1,n+1):
        t_proc = Process(target=multiprocessing_task_q, args=(q,))
        tp.append(t_proc)
        t_proc.start()
    a=[]
    while len(a)!=n:
        z=q.get()
        if z!=None:
            a.append(z)
    q=0
    for i in tp:
        i.join()

    t1=time.time()

    return t1-t

def run_multiprocess_pool(n):
    t=time.time()
    p=Pool(n)
    p.map(multiprocessing_task,range(n))
    p.close()
    p.join()
    t1=time.time()

    return t1-t
    
def system_multiprocess_test():
    x=range(1,17)
    y=[]
    y1=[]
    for i in x:
        y.append(run_multiprocess_process(i))
        y1.append(run_multiprocess_pool(i))

    plt.figure(3)
    plt.plot(x,y,x,y1)
    plt.grid()
    plt.show(block=False)

    return (x,y),(x,y1)

############## BODY

if __name__ == '__main__':
    plot1,plot2=system_subprocess_test()
    plot3=system_thread_test()
    plot4,plot5=system_multiprocess_test()
    plt.figure(4)
    plt.plot(plot1[0],plot1[1],'x--',markersize=8,mew=2)
    plt.plot(plot2[0],plot2[1],'x--',markersize=8,mew=2)
    plt.plot(plot3[0],plot3[1],'x--',markersize=8,mew=2)
    plt.plot(plot4[0],plot4[1],'x--',markersize=8,mew=2)
    plt.plot(plot5[0],plot5[1],'x--',markersize=8,mew=2)
    plt_stats()
    plt.xlabel('task number', fontsize=20)
    plt.ylabel(r's', fontsize=20,rotation=0)
    plt.legend((("subprocess_readline"),('subprocess_communicate'),('threads'),('multiprocess_process'),('multiprocess_pool')), loc='upper left', fontsize=16)
    plt.grid(True)
    plt.show()

# Commit pushed through sourcetree
# successfully merged
