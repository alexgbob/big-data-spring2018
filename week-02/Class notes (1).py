#BRANCHING
flag=1
if flag ==1:
    x=1
    print ("Flag is true.")
else:
    x=2
    print ("Flag is false.")
print(x)

x=range(10)
x=[1,2,3,4,5,6,7,8,9]
for i in x: #pass every value through the interator
    print(i)

for i in x:
    print (i*2)

for i in x:
    if (i > 5):
        break #means stop
    print(i)

my_list = ['This', 'is', 'python']
for i in my_list:
    print (i)
    print (my_list.index(i)) #for every string, it shows what index number is corresponds to

x=0
for i in range(100):
    x+= i # equivalent to x+i, its shorthand
print (x)

# a stored block of code using variabled

def for_sum(x,y):
        for i in range(y):
            x+=i
            return x

#VECTORIZATION
import numpy as np

a=[1,2,3,4,5]
b=[6,7,8,9,10]
c=[]

for i, j in zip(a,b):
    c.append(i+j)
print(c) [7,9,11,13,15]

a = np.array ([1,2,3,4,5])
b = np.array([6,7,8,9,10]) #need to have arrays of the same length
c = a + b
