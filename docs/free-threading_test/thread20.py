import sys
import time, random
from concurrent.futures import ThreadPoolExecutor

try:
    _is_gil_enabled = sys._is_gil_enabled()
except:
    _is_gil_enabled = True

print(f"Gil Enabled = {_is_gil_enabled}")

def fib(n):
    if n < 2: return 1
    return fib(n-1) + fib(n-2)

threads = 20
start = time.perf_counter()
if len(sys.argv) > 1:
    threads = int(sys.argv[1])

with ThreadPoolExecutor(max_workers=threads) as executor:
    for _ in range(threads):
        executor.submit(lambda: print(fib(34)))
t = time.perf_counter()-start
print("Solved g %.2f secs " %t) 
