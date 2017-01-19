import time
t=time.time()
k=0
for i in range(10000000):
    k=k+1
t1=time.time()
print(t1-t)
