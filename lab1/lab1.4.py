import time
import matplotlib.pyplot as plt
from decimal import Decimal, Context, ROUND_HALF_EVEN

def fib(x):

    ctx = Context(prec=60, rounding=ROUND_HALF_EVEN)
    
    sqrt5 = Decimal(5)**Decimal('0.5')
    phi = Decimal(1 + sqrt5)
    phi2 = Decimal(1 - sqrt5)
    
    numerator = ctx.power(phi, Decimal(x)) - ctx.power(phi2, Decimal(x))
    denominator = Decimal(2**x) * sqrt5
    
    return int(numerator / denominator)

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
plt.title("Binet Formula Fibonacci Method")
plt.xlabel("n-th Fibonacci Term")
plt.ylabel("Time (s)")
plt.grid(True)
plt.show()