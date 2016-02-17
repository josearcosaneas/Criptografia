# -*- coding: utf-8 -*-
"""
Created on Sat Aug 30 01:28:35 2014

@author: blunt
"""
import random

def eucExt(a,b):
    r = [a,b]
    s = [1,0] 
    t = [0,1]
    i = 1
    q = [[]]
    while (r[i] != 0): 
        q = q + [r[i-1] // r[i]]
        r = r + [r[i-1] % r[i]]
        s = s + [s[i-1] - q[i]*s[i]]
        t = t + [t[i-1] - q[i]*t[i]]
        i = i+1
    return (r[i-1], s[i-1], t[i-1])
 

def modexp(y, x, n):
  a = x
  b = 1
  c = y
  while a != 0:
    if a % 2 == 0:
      a = a/2
      c = (c**2) % n
    else:
      a = a -1
      b = (b * c) % n
  return b
  
def Ejercicio6():
    n=50000000385000000551
    d=5
    e=10000000074000000101
    de=d*e
    a=0
    b=de-1
    print "de-1 = 2^a * b"

    while(b%2 == 0):
        a=a+1

        b=b/2

    #random x: 0 < x < N
    x=random.randint(1,n)
    #gcd(x,n)
    gcd,u,v=eucExt(x,n)

    if (gcd!=1):
        print "x es factor de n"
    else:

        y=modexp(x,b,n)
        z=0
        print y
        if(y==1 or y==n-1):
            print "fail1"            
        else:
            while(y!=1 or y!=n-1):
                z=y
                y=modexp(y,2,n)             
            if(y==n-1):
                print "fail2"
            elif(y==1):
                p,u,v=eucExt(n,z+1)
                q,u,v=eucExt(n,z-1)
                print "p ",p,"*", "q",q," = ", p*q
Ejercicio6()
        
    
    