import time
import matplotlib.pyplot as plt

def fib(n):
    if n <= 1:
        return n
    else:
        return fib(n-1) + fib(n-2)

A = [5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30]
execution_times = []

for i in A:
    start = time.time()
    result = fib(i) 
    end = time.time()
    execution_times.append(end - start)

print("      ", end="") 
for val in A:
    print(f"{val:>8}", end="")
print() 

print("      ", end="") 
for t in execution_times:
    print(f"{t:>8.4f}", end="")
print("\n")

plt.plot(A, execution_times, marker='o', color='b')
plt.title("Recursive Fibonacci Function")
plt.xlabel("n-th Fibonacci Term")
plt.ylabel("Time (s)")
plt.grid(True)
plt.show()