import time
import matplotlib.pyplot as plt

def fast_doubling(n):
    if n == 0:
        return (0, 1)
    else:
        a, b = fast_doubling(n >> 1)
        c = a * (b * 2 - a)
        d = a * a + b * b
        if n & 1:
            return (d, c + d)
        else:
            return (c, d)

def fib(n):
    return fast_doubling(n)[0]

A = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]
execution_times = []

for i in A:
    start = time.time()
    result = fib(i)
    end = time.time()
    execution_times.append(end - start)

print("      ", end="") 
for val in A:
    print(f"{val:>10}", end="")
print() 

print("      ", end="") 
for t in execution_times:
    print(f"{t:>10.4f}", end="")
print("\n")

plt.plot(A, execution_times, marker='o', color='tab:blue')
plt.title("Fast Doubling Fibonacci Method")
plt.xlabel("n-th Fibonacci Term")
plt.ylabel("Time (s)")
plt.grid(True)
plt.show()