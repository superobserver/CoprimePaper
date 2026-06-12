import math
import cmath
from math import gcd
from functools import reduce

# TP Proof 
#Composite Class model for fusion set of amplitude features across several classes. Includes hole extinction at thresholds of multiclass marking.

def lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0

def lcm_list(nums):
    return reduce(lcm, nums, 1)

def drLD(x, l, m, z, list_amp, primitive, limit):
    y = 90 * (x * x) - l * x + m
    if y < 0 or y >= limit:
        return
    list_amp[int(y)] += 1
    p = z + (90 * (x - 1))
    if p <= 0:
        return
    n = 1
    while True:
        next_y = y + p * n
        if next_y >= limit:
            break
        list_amp[int(next_y)] += 1
        n += 1

def get_operators(k):
    R = [1,7,11,13,17,19,23,29,31,37,41,43,47,49,53,59,61,67,71,73,77,79,83,89]
    operators = []
    for z in R:
        o = (k * pow(z, -1, 90)) % 90
        z_eff = 91 if z == 1 else z
        o_eff = 91 if o == 1 else o
        l = 180 - (z_eff + o_eff)
        m = 90 - (z_eff + o_eff) + (z_eff * o_eff - k) // 90
        operators.append((l, m, z_eff, k))
    return operators

def run_sieve(h, classes):
    epoch = 90 * (h * h) - 12 * h + 1
    a = 90
    b = -300
    c = 250 - epoch
    d = (b**2) - (4*a*c)
    sol2 = (-b + cmath.sqrt(d)) / (2*a)
    new_limit = int(sol2.real) + 1
    list_amp = [0] * (epoch + 100)
    all_ops = []
    for k in classes:
        all_ops.extend(get_operators(k))
    for x in range(1, new_limit + 1):
        for op in all_ops:
            drLD(x, *op[:3], list_amp, op[3], epoch)
    list_amp = list_amp[:epoch]
    holes = [i for i, amp in enumerate(list_amp) if amp == 0]
    return len(holes), holes

# Example usage: Compute holes for custom class combos up to h=30
classes5 = [11, 17, 23, 29, 41]  # Example 5-class combo
classes7 = [11, 17, 23, 29, 41, 47, 53]  # Example 7-class combo
for h in range(1, 31):
    holes5, _ = run_sieve(h, classes5)
    holes7, _ = run_sieve(h, classes7)
    print(f"h={h}: 5-classes holes={holes5}, 7-classes holes={holes7}")
