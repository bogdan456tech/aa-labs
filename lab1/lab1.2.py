import time
import matplotlib.pyplot as plt

def f(x):
    l1 = [0, 1]
    for i in range(2, x + 1):
        l1.append(l1[i-1] + l1[i-2])
    return l1[x]

A = [501, 631, 794, 1000,
1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]
execution_times = []

for i in A:
    start = time.time()
    result = f(i) 
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
plt.title("Dynamic Programming Fibonacci Function")
plt.xlabel("n-th Fibonacci Term")
plt.ylabel("Time (s)")
plt.grid(True)
plt.show()