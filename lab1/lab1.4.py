# Full working example: Correct Binet formula + timing + graph

import time
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext, ROUND_HALF_EVEN

def fib(n):
    getcontext().prec = 60
    getcontext().rounding = ROUND_HALF_EVEN

    sqrt5 = Decimal(5).sqrt()
    phi = (Decimal(1) + sqrt5) / Decimal(2)
    psi = (Decimal(1) - sqrt5) / Decimal(2)

    value = (phi ** n - psi ** n) / sqrt5
    return int(value.to_integral_value())

A = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]
execution_times = []

for i in A:
    start = time.time()
    fib(i)
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

plt.figure()
plt.plot(A, execution_times, marker='o')
plt.title("Binet Formula Fibonacci Method (Decimal)")
plt.xlabel("n-th Fibonacci Term")
plt.ylabel("Time (seconds)")
plt.grid(True)
plt.show()
