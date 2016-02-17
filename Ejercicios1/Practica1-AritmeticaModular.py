# -*- coding: utf-8 -*-
"""

@fecha:
    
@author: José Arcos Aneas                                   @DNI: 74740565-H

@asignatura: Criptografia.

                       PRÁCTICA-1 ARITMÉTICA MODULAR

"""   
print "Guion De Ejercicios de Criptografia"
print "Practica 1 Aritmetica modular"
# Librerias a usar

import time
import random
import math
from math import sqrt, ceil

import operator

############################################################################
# Funcion 'cronometro' se usa para controlar el tiempo de ejecucion de una 
# funcion.                                                                         
# tiempo3 = cronometro(funcion)(parametros)                                                                         
# la libreria time dispone de dos posibilidades a la hora de medir tiempos de 
# ejecucion time.time() y time.clock, la diferencia es que time.clock es mucho
# mas preciso ya que solo mide el tiempo de CPU gastado.                                  
############################################################################
def cronometro(funcion):
   def funcion_a_ejecutar(*argumentos):
       # Tiempo de inicio de ejecución.
       inicio = time.clock()
       # Lanzamos función a ejecutar.
       ret = funcion(*argumentos)
       # Tiempo de fin de ejecución.
       fin = time.clock()
       # Tiempo de ejecución.
       tiempo_total = fin - inicio
       # Devolvemos el tiempo de ejecución.
       return tiempo_total
   # Devolvemos la función que se ejecuta.
   return funcion_a_ejecutar
   


"""
Ejercicio 1 

Implementacion del algoritmo extendido de Euclides


"""
############################################################################

############################################################################
   
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)



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
##
##   Bateria de prueba para el ejercicio
##
 
a=124815345435432523523523453426342623132542
b=5236234

print "*--*"*15
print ""
print "Ejecutando ejercicio 1. Algoritmo extendido de Euclides." 
print "Valores a,b:", a ,b 
print "Resultado:", eucExt(124815345435432523523523453426342623132542,5236234)
tiempo= cronometro(eucExt)(124815345435432523523523453426342623132542,5236234)

print "El tiempo de ejecucion es :", tiempo 

print "*--*"*15
print ""
   


"""
Ejercicio 2. Calculo del inverso multiplicativo modular.


"""   
############################################################################
              
############################################################################
   
def modinv(a, m):

    g, x, y = eucExt(a, m)
    if g != 1:
        raise Exception('No existe el inverso.')
    else:

        return x % m
        
        
##
##   Bateria de prueba para el ejercicio
##
        
print "*--*"*15
print ""
a=391
m=1542

print "Ejecutando ejercicio 2. a^-1 mod m" 
print "Valores a , m: ",a,m
print "El resultado es:" ,modinv(a,m)

tiempo= cronometro(modinv)(a,m)
print "El tiempo de ejecucion del algoritmo es:", tiempo
print "*--*"*15
print ""
   
"""
Ejercicio 3. Exponenciacion modular


"""   
############################################################################
              
############################################################################


def binconvert(n):
  barray = []
  if n < 0: return
  if n == 0:
    return 0
  while n > 0:
    barray.append(n%2)
    n = n >> 1#cociente debe ser mas rapido el resto lo podemos poner asi n&1 
  barray.reverse()
  return barray
# Esta es la forma iterativa que es mas lenta
def modexp(base, pow, mod):

  exponent = 1
  i = 0
  while i < pow:
    exponent = (exponent * base) % mod  
    i += 1
  return exponent
#y**x mod n
def modexp1(y, x, n):
  #convertimos previamente x en una lista de bits
  x = binconvert(x)
   
  s = [1]
  r = x[:]
  for k in range (0, len(x)):
    if x[k] == 1:
      r[k] = (s[k] * y) % n
    else:
      r[k] = s[k]
    s.append ((r[k]**2)%n)
  #print s
  #print r
  return r[-1]
# Esta es la que piden en la practica
# similar to modexp1 excepto que este lo hace con los bits 
# a la inversa
def modexp2(y, x, n):
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
##
##   Bateria de prueba para el ejercicio
##

print "*--*"*15
print ""

print "Ejercicio 3. y^x mod n  "
y=198372606439612624903621097679236901246097612903467
x=10000000

n=3
print "Tiempo de mod exp de forma iterativa:", cronometro(modexp)(y,x,n)

print "Tiempo de mod exp1 convirtiendo la cadena: "
print "y haciendolo en orden correcto", cronometro(modexp1)(y,x,n)
print modexp1(y,x,n)
print "Tiempo de mod exp2. Forma mas eficiente convirtiendo a base dos"
print "y calculando en orden inverso a mod exp1:", cronometro(modexp2)(y,x,n)

print "*--*"*15

"""

Ejercicio 4 . Test de primalidad de Miller-Rabin


"""   
############################################################################
              
############################################################################

 # Esta implementacion de Miller-Rabin funciona a partir de p = 5
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
			a = modexp2(a, s, p) # a = a^s en modulo p 
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
##
##   Bateria de prueba para el ejercicio
##

p=38771810603
n=10
   
print "*--*"*15
print ""
print "Ejercicio 4. Test de primalidad de Miller-Rabin"
print "Valor del numero al que pasarle el test",p
print "Numero de repeticiones del Test", n
print "Resultado del algoritmo",test_Rabin(p,n)
print "Tiempo de ejecucion", cronometro(test_Rabin)(p,n)
print "*--*"*15
print ""



"""
Ejercicio 5. Algorimto para el calculo del logaritmo discreto.

    Algoritmo del paso gigante paso enano
"""   
############################################################################
              
############################################################################
   
def Paso_Gigante_Paso_Enano(y , a ,n):
    s = int(math.floor(sqrt(n)))
 
    A = []
    B = []
 
    for r in range(0,s):
        value = y*(a^r) % n
        A.append(value)

 
    for t in range(1,s+1):
         value = a^(t*s) % n
         B.append(value)

    print A
    print B
 
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
##
##   Bateria de prueba para el ejercicio
##


y=7
a=2
n=131
print "*--*"*15
print ""
print "Ejercicio 5. Implementacion del algoritmo Paso Gigante Paso Enano"
print "Valores de y,a,n",y,a,n
print "El resultado del algoritmo",Paso_Gigante_Paso_Enano(y , a , n)
print "Tiempo de ejecucion del algoritmo:", cronometro(Paso_Gigante_Paso_Enano)(y,a,n)

print "*--*"*15
print ""




"""
Ejercicio 6. Sea n = n*p 
    a) Escribir funcion q dado un entero y un primo devuelva r tal q r^2 conf
    con a mod p
    
    

"""   
############################################################################
   #  a) Escribir funcion q dado un entero y un primo devuelva r tal que:
   #                           r^2=a mod p          
############################################################################
def modular_sqrt(a, p):

    # caso base
    #
    if Jacobi(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return modexp2(a, (p + 1) / 4, p)

    # Partir p-1 en s*2^e * s odd 
  
    s = p - 1
    e = 0
    while s % 2 == 0:
        s /= 2
        e += 1

    # Buscar con legendre o jacobi n talque n|p = -1.

    n = 2
    while Jacobi(n, p) != -1:
        n += 1

    x = modexp2(a, (s + 1) / 2, p)
    b = modexp2(a, s, p)
    g = modexp2(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in xrange(r):
            if t == 1:
                break
            t = modexp2(t, 2, p)

        if m == 0:
            return x

        gs = modexp2(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m
    return r
#Version recursiva
def Jacobi1(a,p):
    if a==0: return 0
    if a==1: return 1
    a1=a 
    e = 0
    while a1 % 2 == 0:
        a1 /= 2
        e += 1
    if e & 1==0:
        s=1
    else :
        if operator.mod(p,8)==1 or operator.mod(p,8) == 7: s =1
        if  operator.mod(p,8)==3 or operator.mod(p,8) == 5: s =-1
    
    if (operator.mod(p,4)== 3 and operator.mod(a1,4)==4): s=-s
    p1=operator.mod(p,a1)
    if(a1==1): return s
    else: return (s*Jacobi1(p1,a1))
# Version iterativa
def Jacobi(a, n) : 
    r = 1 
    while a <> 0 : 
        if a < 0 : 
            a = -a 
            if operator.mod(n, 4) == -1 : 
                r = -r 
        while a%2==0: 
            a = a / 2 
            m = operator.mod(n, 8) 
            if m == 3 or m == -3 : 
                r = -r 
        ma = operator.mod(a, 4);
        mn = operator.mod(n, 4) 
        if ma == -1 and mn == -1 :
            r = -r 
        t = a; 
        a = n - a * ceil(n/a - 1/2); 
        n = t 

    return 0 if n > 1 else r
##
##   Bateria de prueba para el ejercicio
##

print "*--*"*15
print ""
a=5
p=299
print "Ejercicio 6."
print "-"*60
print "Apartado a)"
print "Comprobamos el valor del simbolo de jacobi para a y p:",a , p
print "Calculo iterativo. ","Resultado:",Jacobi(a,p),"Tiempo de ejecucion:",cronometro(Jacobi)(a,p) 
print "Calculo recursivo. ","Resultado:",Jacobi1(a,p),"Tiempo de ejecucion:",cronometro(Jacobi1)(a,p) 
print "Calculo de raices cuadraticas:"
print "Valores de a,p:",a,p
print "El resultado del algoritmo",modular_sqrt(a,p)
print "Tiempo de ejecucion del algoritmo:", cronometro(modular_sqrt)(a,p)

print ""

############################################################################
# Apartado B
############################################################################
def modular_sqrt_comp(a, n , p, q):
    r=modular_sqrt(a,p)
    s=modular_sqrt(a,q)
    print " Raices de p y q respectivamente"
    print [r,-r%p],[s,-s%q]
    ap= (q*modinv(q,p))%n
    aq= (p*modinv(p,q))%n

    x = ((ap*r + aq*s))%n
    y = ((ap*r - aq*s))%n
    
    return x,-x%n ,y, -y%n
    
##
##   Bateria de prueba para el ejercicio
##

print "-"*60
print "Apartado b)"
a=132
n=493
p=17
q=29
print " Calculo de las raices modulares de a en n=p*q" 
print " Valores para a,n,p,q: ",a,n,p,q
print " Resultado:",modular_sqrt_comp(a,n,p,q)
print " El tiempo de ejecucion del algoritmo es :", cronometro(modular_sqrt_comp)(a,n,p,q)
print "-"*60
"""
Ejercicio 7.  Factorizacion de enteros.

    a) Factorizacion de Fermat
    
    b) Factorizacion p de Pollard
"""   


############################################################################
#  a) factorizacion de Fermat       
############################################################################

def fermat(n):
    a = int(ceil(n**0.5))
    b2 = a*a - n
    b =  int(b2**0.5)
    
    while b*b != b2:
        print('Probando: a=%s b2=%s b=%s' % (a, b2, b))
        a = a + 1 # aumentamos en uno 
        b2 = a*a - n # recalculamos  b2
        b =  int(b2**0.5) 
        
    # Calculamos p y q
    p=a+b
    q=a-b

    assert n == p * q
    print "Valores para  a ,b, p=a+b ,q=a-b, p*q:", a ,b, p ,q,p*q

    print "Resultado:", p, q
    return
##
##   Bateria de prueba para el ejercicio
##

print "*--*"*15
print ""
print "Ejercicio 7."
print "-"*60
print ""
print "Apartado A)"
n=40259
print "Factorizacion de Fermat" 
print " Valor de prueba",n
print "Tiempo de ejecucion del algoritmo",cronometro(fermat)(n)

print "*--*"*15
print ""

############################################################################
#  b) Factorizacion rho de Pollard            
############################################################################

    
	
def rho_de_pollard(n):
     
 
    if n==None: return 1
    f = lambda x: (x**2+1)%n
    a = random.randint(1, n - 1) # a al azar entre 1 y n-1 (ambos inclusive)
    x = f(a)
    y = f(x)
    i = 1
    I = 1000 # Número máximo de iteraciones
    if (n & 1==0): return 2
    if (n%3==0): return 3
    if (n%5==0):return 5
    while i != I:
        d,v,u = eucExt(y-x, n)
        if d == 1:
            i = i + 1
            x = f(x)
            y = f(f(y))
        else:
            return d
	
	return None
 


def pollard(n):
    if (n & 1==0): return 2
    if (n%3==0): return 3
    if (n%5==0):return 5
    a=random.randrange(1,n-1)
    x=a*a+1
    y=x*x+1
    for i in range(1,1000):
        d,v,u=eucExt(y-x,n)
        if d==n : 
            return n
        if d==1:        
            i=i+1
            x=(x*x+1)%n
            y=((y*y+1)+1)%n
        return d
    return n
    

##
##   Bateria de prueba para el ejercicio
##
 


print "-"*60
print ""
print "Apartado B)"
n=13*38771810603*19*7*3
print " Valor de prueba",n
print " Resultado de aplicar el algoritmo p de pollard es:",rho_de_pollard(n)
print "El tiempo de ejecucion del algoritmo es de :",cronometro(rho_de_pollard)(n)
print "-"*60

    
print "==="*15
