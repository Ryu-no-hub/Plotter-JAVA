import matplotlib.pyplot as plt
import pandas as pd
import statistics


def median_softening(a, n):
    #n = n
    A = a.copy()
    T = len(A)
    iterations = 0
    for i in range(n, T-n):
        b = []
        #print(i)
        for j in range(i-n, i+n+1):
            iterations+=1
            b.append(A.iloc[j, 0])
        #print(b, 'b len =', len(b))
        A.iloc[i] = statistics.median(b)
    print('n =', n, 'iterations =', iterations)
    return A, iterations

#I(T) = (T-2*n)*(2n+1)
#I(n) = 2*T*n - T - 4*n^2 - 2*n
T1 = pd.DataFrame([30, 31, 33, 36, 20, 37, 37, 37, 38, 40, 49, 40, 41, 42, 42, 42, 42, 41, 40])
T2 = pd.DataFrame([30, 31, 33, 36, 20, 37, 37, 37, 38, 40, 49, 40, 41, 42, 42, 42, 42, 41, 40, 39, 37, 36, 35, 35])
T3 = pd.DataFrame([30, 31, 33, 36, 20, 37, 37, 37, 38, 40, 49, 40, 41, 42, 42, 42, 42, 41, 40, 39, 37, 36, 35, 35, 34, 33, 32, 30, 28])
T4 = pd.DataFrame([30, 31, 33, 36, 20, 37, 37, 37, 38, 40, 49, 40, 41, 42, 42, 42, 42, 41, 40, 39, 37, 36, 35, 35, 34, 33, 32, 30, 28, 26, 24, 22, 23, 20])
T5 = pd.DataFrame([30, 31, 33, 36, 20, 37, 37, 37, 38, 40, 49, 40, 41, 42, 42, 42, 42, 41, 40, 39, 37, 36, 35, 35, 34, 33, 32, 30, 28, 26, 24, 22, 23, 20, 19, 17, 15, 13, 11, 10])

plt.figure()
T1, nt1 = median_softening(T1, 2)
plt.plot(T1, linewidth=2)
T2, nt2 = median_softening(T2, 2)
plt.plot(T2, linewidth=2)
T3, nt3 = median_softening(T3, 2)
plt.plot(T3, linewidth=1)
T4, nt4 = median_softening(T4, 2)
plt.plot(T4, linewidth=1)
T5, nt5 = median_softening(T5, 2)
plt.plot(T5, linewidth=1)
plt.show()

nt = [nt1, nt2, nt3, nt4, nt5]
v = [19, 24, 29, 34, 40]
plt.figure()
plt.plot(v, nt, linewidth=2)
plt.show()

T5, nn0 = median_softening(T5, 1)
T5, nn1 = median_softening(T5, 2)
T5, nn2 = median_softening(T5, 4)
T5, nn3 = median_softening(T5, 6)
T5, nn4 = median_softening(T5, 8)
T5, nn5 = median_softening(T5, 10)
T5, nn6 = median_softening(T5, 12)
T5, nn7 = median_softening(T5, 14)
T5, nn8 = median_softening(T5, 16)
T5, nn9 = median_softening(T5, 19)

nn = [nn0, nn1, nn2, nn3, nn4, nn5, nn6, nn7, nn8, nn9]
w = [1, 2, 4, 6, 8, 10, 12, 14, 16, 19]
plt.plot(w, nn, linewidth=2)
plt.show()