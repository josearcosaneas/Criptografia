# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este archivo temporal se encuentra aquí:
/home/blunt/.spyder2/.temp.py
"""

"""test de primalidad de rabin"""

import random
import math
 
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
    
def GSBS(y , a ,n):
    s = int(math.floor(math.sqrt(n)))
 
    A = []
    B = []
 
    for r in range(0,s):
        value = y*(a^r) % n
        A.append(value)

 
    for t in range(1,s+1):
         value = a^(t*s) % n
         B.append(value)
 
    x1,x2 =0,0
  
    for r in A:
        for t in B:
            if r == t:
                x1 = A.index(r)            
                x2 = B.index(t)
                print " Posiciones en las que se producen las coincidencias:"
                print x1,x2
                break
             
    return ((x2+1)*s - x1) % n # Answer
    
    
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
    
""" calcula los divisores primos"""
def Factorize(n):
    prime_divisors=[]
    i=2
    limit=n
    while(i<=limit):
        if((limit%i)==0 and test_Rabin(i,10)):
            prime_divisors.append(i)
            limit=limit/i
            if(test_Rabin(limit,10)):
                prime_divisors.append(limit)
        else: 
            if ((i%2)==0 ):
                i+=1
            else: 
                i+=2
                
    return prime_divisors
def gcd(a, b): 
    a, b = max(a, b), min(a, b) 
    c = 1
    while c:
        c = a % b 
        a = b 
        b = c 
    return a 

# alpha en Z*_n es un generador o elemento primisivo sii
#  alpha^{phi(n)/p) != 1 mod n
# para cada divisor p de phi(n)
""" Funcion para encontar un elemento primitivo"""
def prim_root(p):
    phi_n=p-1
    prime_divisors=Factorize(phi_n)

    not_gen=1
    while(not_gen==1):
        alpha=random.randint(2,p) 
        i=0
        while i< len(prime_divisors):
            not_gen=modexp(alpha,(phi_n/prime_divisors[i]),p)
            i+=1            
            if not_gen==1:
                break
    return alpha
            
                


#print (prim_root(2343254323))

 
dni=74740565    
birth= 11061990

 
def Ejercicio1(dni,birth):
    dni=NextPrime(dni)
    print dni
    print birth
    alpha=prim_root(dni)
    print alpha
    x = GSBS(birth, alpha,dni)
    f = modexp(alpha,x,dni)
    print x
    print f
Ejercicio1(dni,birth)