# -*- coding:utf-8 -*-
from z3 import *

s = []
for i in range(24):
    s.append(Int('S'+str(i)))
x = Solver()

# 0
x.add(s[0]+s[0]+22 == 252)
# 1
x.add(s[0]+s[18]+s[1]+23 == 352)
# 2
x.add(s[0]+s[18]+s[6]+s[2]+85 == 484)
# 3
x.add(s[0]+s[18]+s[6]+s[3]+85 == 470)
# 4
x.add(s[0]+s[18]+s[6]+s[21]+s[4]+35 == 496)
# 5
x.add(s[0]+s[18]+s[6]+s[21]+s[5]+35 == 487)
# 6
x.add(s[0]+s[18]+s[6]+s[21]+s[12]+s[6]+27 == 539)
# 7
x.add(s[0]+s[18]+s[6]+s[21]+s[12]+s[7]+27 == 585)
# 8
x.add(s[18]+s[6]+s[21]+s[12]+s[8]+5 == 447)
# 9
x.add(s[18]+s[6]+s[21]+s[12]+s[15]+s[9]-91 == 474)
# 10
x.add(s[18]+s[6]+s[21]+s[12]+s[15]+s[9]+s[10]-105 == 577)
# 11
x.add(s[18]+s[21]+s[12]+s[15]+s[9]+s[11]-167 == 454)
# 12
x.add(s[18]+s[21]+s[12]+s[15]+s[9]+s[12]-167 == 466)
# 13
x.add(s[18]+s[21]+s[15]+s[9]+s[13]-159 == 345)
# 14
x.add(s[18]+s[21]+s[15]+s[9]+s[14]-159 == 344)
# 15
x.add(s[18]+s[21]+s[15]+s[9]+s[3]+s[15]-113 == 486)
# 16
x.add(s[18]+s[21]+s[15]+s[9]+s[3]+s[16]-113 == 501)
# 17
x.add(s[18]+s[15]+s[9]+s[3]+s[17]-63 == 423)
# 18
x.add(s[18]+s[15]+s[9]+s[3]+s[18]-63 == 490)
# 19
x.add(s[15]+s[9]+s[3]+s[19]-64 == 375)
# 20
x.add(s[15]+s[3]+s[20]-50 == 257)
# 21
x.add(s[3]+s[21]+46 == 203)
# 22
x.add(s[3]+s[22]+46 == 265)
# 23
x.add(s[23] == 125)

if(x.check()==sat):
    model = x.model()
    print(model)

model = x.model()

flag = [0]*24

for i in str(model).split(','):
    pos, val = i.split('=')[:2]
    pos = int(''.join([i for i in pos if i.isdigit()]))
    val = int(''.join([i for i in val if i.isdigit()]))
    flag[pos] = chr(val)

flag = ''.join(flag)

print(flag)
