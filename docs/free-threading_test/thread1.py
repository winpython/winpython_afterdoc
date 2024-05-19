import sys
import time, random
from concurrent.futures import ThreadPoolExecutor

print(f"nogil={getattr(sys.flags, 'nogil', False)}")

def fib(n):
    if n < 2: return 1
    return fib(n-1) + fib(n-2)

threads = 1
start = time.time()
if len(sys.argv) > 1:
    threads = int(sys.argv[1])

with ThreadPoolExecutor(max_workers=threads) as executor:
    for _ in range(threads):
        executor.submit(lambda: print(fib(34)))
t = time.time()-start
print("Solved g %.2f secs " %t) 
