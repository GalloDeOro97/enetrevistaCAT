import numpy as np 

def fizzbuzz(x):
    y = []
    for i in x:
        if i%3 ==0 and i%5 ==0:
            y.append("fizzbuzz")
        elif i%3 == 0:
            y.append("fizz")
        elif i%5 == 0: 
            y.append('buzz')
        else:
            y.append(i)
    return y


vinicial = [1,2,3,4,5,15]
print(fizzbuzz(vinicial))
