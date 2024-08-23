import numpy as np 

def fizzbuzz(x):
    for i in x:
        i=int(i)
        if(i%3 == 0):
            print('Fizz')
        if(i%5 == 0): 
            print('buzz')
        if(i%3 == 0  and i%5 == 0 ):
            print('Fizzbuzz')
        else:
            print(i)


n=input('Introduzca cuantos numero se van a evaluar: ')
x = []
for j in range(int(n)):
    x.append(input())

print(fizzbuzz(x))
