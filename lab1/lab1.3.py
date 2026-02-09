import time
import matplotlib.pyplot as plt

def multiply(F, M):
    x = (F[0][0] * M[0][0] + F[0][1] * M[1][0])
    y = (F[0][0] * M[0][1] + F[0][1] * M[1][1])
    z = (F[1][0] * M[0][0] + F[1][1] * M[1][0])
    w = (F[1][0] * M[0][1] + F[1][1] * M[1][1])
    
    F[0][0] = x
    F[0][1] = y
    F[1][0] = z
    F[1][1] = w

def power(F, n):
    M = [[1, 1], [1, 0]]
    for i in range(2, n + 1):
        multiply(F, M)

def fibb(n):
    F = [[1, 1], [1, 0]]
    if n == 0:
        return 0
    power(F, n - 1)
    return F[0][0]

A = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]
execution_times = []

for i in A:
    start = time.time()
    result = fibb(i)
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
plt.title("Matrix Power Fibonacci Method")
plt.xlabel("n-th Fibonacci Term")
plt.ylabel("Time (s)")
plt.grid(True)
plt.show()