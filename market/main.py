from scipy import optimize
import numpy as np

c = 40
T = 4.3
n = np.floor(T)
t = T - n
p = 500
par = 1000

get_yield = lambda r: (c / r) - (c / r * np.power((1 + r), n)) + (c + par) / np.power((1 + r), n) - p


print(optimize.newton(get_yield, 0.05))

print(t)