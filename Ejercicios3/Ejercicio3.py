# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 18:22:38 2014

@author: blunt
"""

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
n=48478872564493742276963
x=37659670402359614687722
y=12

d=0
u=0
v=0
if ((x%n)!= y and (x%n) != (n-y)):
    d,u,v=eucExt(x-y,n)
    
p=int(n/d)
q=d
print p , q
nc=p*q
print nc
