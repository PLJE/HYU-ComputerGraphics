import numpy as np

#A
M = np.arange(2,27)
print(M)

#B
M = M.reshape(5,5)
print(M)

#C
M[1:4 , 1:4] = np.zeros((3,3))
print(M)

#D
M=M@M
print(M)

#E
v=M[0:1 , :]
tot=0
for i in range(5):
    tot= tot +(v[0][i]* v[0][i])
print(np.sqrt(tot))
