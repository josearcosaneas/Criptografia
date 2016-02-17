# -*- coding: utf-8 -*-
"""
Editor de Spyder


"""
import numpy as np
from math import ceil
import operator



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
            
import random
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
def mcd(n,m):
 m_aux = n%m
 if( m_aux == 0 ):
  return m
 elif( m_aux == 1 ):
  return 1
 else:
  return mcd(m,m_aux)
  
def inv_mult(a,n):
 if(mcd(a,n)!=1):
  print(str(a) + " NO TIENE INVERSO MULTIPLICATIVO EN " + str(n))
 else:
  for i in range(1,n) :
   if( ( a*i-1 )%n == 0 ):
    return i
    
    
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

   


   
def modinv(a, m):

    g, x, y = eucExt(a, m)
    if g != 1:
        raise Exception('No existe el inverso.')
    else:

        return x % m
        
########################################################################
########################################################################
#   Ejercicio1    
########################################################################
########################################################################

class Mochila():
    def __init__(self,clave_privada,n,m):
        self.privada=[]
        self.privada = clave_privada
        self.m=m
        self.n=n
        self.publica=self.generar_publica()
        self.tam=len(self.privada)
		
    def generar_publica(self):
         publicap=[]
         tam=len(self.privada)
         print "Generando llave publica"
         for i in range(0,tam):
             publicap.append((self.privada[i]*self.n)%self.m)
         print "la llave publica es:"
         return publicap

    def cifrar(self, mensaje):
        numeroSubconjuntos = len(mensaje)/self.tam
       
        mensaje=np.array(mensaje)
        mensaje = mensaje.reshape(numeroSubconjuntos,self.tam)
        solucion=[]

        for i in range(0,numeroSubconjuntos):
            valor=0
            for j in range(0, self.tam):
            
                if mensaje[i][j]== 1:
                    valor= valor +  self.publica[j]
            solucion.append(valor)
        
        return solucion				
            
            
    def descifrar(self,mensaje):
        inv_n=inv_mult(self.n,self.m)
        nueva_clave=[]
        for i in range(0,len(self.publica)):
            nueva_clave.append((self.publica[i]*inv_n)% self.m)
        aux_men=[]

        for i in range(0,len(mensaje)):
            aux_men.append((mensaje[i]*inv_n)%self.m)
       
        solucion_final=[]

        
        for i in range (0,len(aux_men)):
            solucion_parcial=[]
            aux=aux_men[i]
            j=0
            index=len(self.privada)-1
            while (index >=0 or aux > 0):
                maximo=self.privada[index]
                if aux>=maximo:
                    aux=aux-maximo
                    solucion_parcial.append(1)
                else:
                    solucion_parcial.append(0)
                j=j+1
                index=index-1
            solucion_parcial.reverse()
         

            solucion_final.append(solucion_parcial)
        return solucion_final
"""
Cifa el mensaje 
Primro crea un numero de subconjuntos dependiendo del tamaño del mensaje y el tamaño de las claves
Despues para cada subconjunto calculamos su valor cifrado
Si hay un uno se coje el valor de la cadena publica que  corresponda con la misma posicion sino se ignora
"""	

## Bateria de prubas
clave=[1,2,4,10,20,40]
m=110
n=31
mensaje=[1,0,0,1,0,0,1,1,1,1,0,0,1,0,1,1,1,0]
mochila=Mochila(clave,n,m)

mensaje_cifrado=mochila.cifrar(mensaje)
mensaje_descifrado=mochila.descifrar(mensaje_cifrado)
print "Mensaje"
print mensaje
print "Mensaje cifrado"
print mensaje_cifrado
print "Mensaje descifrado"
print mensaje_descifrado

########################################################################
########################################################################


    
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

#print "-"*60
#
#a=132
#n=493
#p=17
#q=29
