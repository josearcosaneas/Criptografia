# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 18:32:39 2014

@author: blunt
"""
import random

#algorimto extendido de euclides
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
 
# test de primmalidad de Rabin
def test_Rabin(p,n=10):
	if p & 1 == 0:
		return False

	if p < 6:
		return p in [2,3,5]
	
	else:
		primo = True	
		u = 0
		s = p - 1
		while(s & 1 == 0): # Expresar p-1 como (2^u)*s, s impar
			u = u + 1
			s = s / 2
			
		for rondas in range(n):
			a = random.randint(2, p - 2) # a al azar entre 2 y p-2 incluidos
			a = modexp(a, s, p) # a = a^s en modulo p 
			if a == 1 or a == (p - 1): # si a = 1 ó a = p-1
				primo = True  # p probable primo
			else:
				i = 1
				while i != u : #desde i = 1 hasta u-1
					a = (a * a) % p	
					if a == (p - 1):
						primo = True # p es probable primo
						break
					elif a == 1:
						primo = False # p no es primo
						break
					
					i = i + 1
				
				if i == u:
					primo = False # p no es primo
				
			if primo == False:
				break # Si ya se ha determinado que no es primo, parar el bucle de rondas

		return primo
""" calcula el siguiente primo"""
def NextPrime(p):
    if p%2==0:
        p=p+1

    while( not test_Rabin(p)):
        p+=2
    return p
"""Exponenciacion modular"""
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
dni=74740565    
birth= 11061990
x=1234567890

def Ejercicio4(dni,birth,x):
    p=NextPrime(dni)
    print p
    q=NextPrime(birth)
    phi_n=(p-1)*(q-1)
    print q    
    n=p*q
    e=3
    d,u,v= eucExt(e,phi_n)
    while(d!=1):
        e = random.randint(2,p)
        d,u,v=eucExt(e,phi_n)
    d=u%phi_n
    print "con de igual  a ", d
    # d = e^-1 mod phi(n)
    rsa_inv=modexp(x,d,n)
    return rsa_inv

    
a=Ejercicio4(dni,birth,123456789)
print a
    
    
    
    
    
    
    
    
    
    
    
