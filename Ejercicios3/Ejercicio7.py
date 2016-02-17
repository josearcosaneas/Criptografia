# -*- coding: utf-8 -*-
"""
Created on Sat Aug 30 14:26:35 2014

@author: blunt
"""

#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import struct
import random

try:
    range = xrange
except NameError:
    pass

"""Get Random Bits
Generates a sequence of random bits of a random size between 1 and 1000
bits in the sequence.
Returns:
A stream of random bits.
"""
def get_random_bytes():

    size = random.randrange(1, 1000)
    for _ in range(size):
        yield random.getrandbits(8)

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
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('no existe')
    else:
        return x % m
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
 return r[i-1]
def genprime(bitn,k=10):
    prime=random.randint(2**bitn-1,2**bitn)
    if prime%2==0:
        prime+=1
    while not(test_Rabin(prime,k)):
        prime+=2
    return prime
    
def genkeys(bitn):
    p=genprime(bitn)
    q=genprime(bitn)
    n=p*q
    phi=(q-1)*(p-1)
    e=65537
    while phi%e==0:
        e=genprime(17)
    d=modinv(e,phi)
    public=[n,e]
    private=[n,d]    
    return public,private
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
    
    
def _left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff
"""
SHA-1 Hashing Function

A custom SHA-1 hashing function implemented entirely in Python.
Arguments:message: The input message string to hash.
Returns:A hex SHA-1 digest of the input message.
Referencia: www.code.google.es
"""
def sha1(message):
    
    # Initialize variables:


    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    # Pre-processing:
    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8
    # append the bit '1' to the message
    message += b'\x80'
    # append 0 <= k < 512 bits '0', so that the resulting message length (in bits)
    # is congruent to 448 (mod 512)
    message += b'\x00' * ((56 - (original_byte_len + 1) % 64) % 64)
    # append length of message (before pre-processing), in bits, as 64-bit big-endian integer
    message += struct.pack(b'>Q', original_bit_len)
    # Process the message in successive 512-bit chunks:
    # break message into 512-bit chunks
    for i in range(0, len(message), 64):
        w = [0] * 80
        # break chunk into sixteen 32-bit big-endian words w[i]
        for j in range(16):
            w[j] = struct.unpack(b'>I', message[i + j*4:i + j*4 + 4])[0]
# Extend the sixteen 32-bit words into eighty 32-bit words:
        for j in range(16, 80):
            w[j] = _left_rotate(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16], 1)
# Initialize hash value for this chunk:
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        for i in range(80):
            if 0 <= i <= 19:
                # Use alternative 1 for f from FIPS PB 180-1 to avoid ~
                f = d ^ (b & (c ^ d))
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6
                a, b, c, d, e = ((_left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff,
                                 a, _left_rotate(b, 30), c, d)
                                 # sAdd this chunk's hash to result so far:
            h0 = (h0 + a) & 0xffffffff
            h1 = (h1 + b) & 0xffffffff
            h2 = (h2 + c) & 0xffffffff
            h3 = (h3 + d) & 0xffffffff
            h4 = (h4 + e) & 0xffffffff
            # Produce the final hash value (big-endian):
        return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)
"""
Procedimiento de firma digital RSA
1.- A hace un resumen (r) del mensaje con una función resumen (por ejemplo MD5 o SHA1)

2.- La firma digital (f) será la codificación del resumen con su clave privada:

f = r^d, mod n

3.- A envía el mensaje junto con la firma f.

4.- B, el receptor, resume el mensaje con la misma función resumen que A, obteniendo r'

5.- B compara: cifra la firma (f) con la pública de A y debe obtener su r'

[f ^e, mod n] debe ser igual a r'

Si son iguales, se puede afirmar que nadie ha modificado el mensaje que A envió.



"""

"""
Genera un resume con la funcion hash (en nuestro caso SHA1)
"""
def GenerarResumen(menssage):
    return sha1(menssage)
"""
Genera la firma con la clave privada del emisor y el resumen realizado 
con la funcion hash
"""
def GenerarFirma(r,d,n):
    return modexp(r,d,n)
"""
Para la verificaion en primer lugar sera necesario generar un nuevo resume (r_prima)
si este valor corresponde con [f ^e, mod n] se puede concluir que la firma se ha 
recibido correctamente.
"""
def VerificarFirma(mensaje,f,e,n):
    r_prima=GenerarResumen(mensaje)
    r_prima=msg2num(r_prima)
    validacion=False
    if modexp(f,e,n)==r_prima:
        validacion=True
    else:
        print ('La fima no es valida o ha sido modificada.')
    return validacion
    

    
"""
Ejemplo de uso de la funcion de firma digital RSA

"""

def msg2num(s):
    n = 0
    for c in s:
        n <<= 8
        n += ord(c)
    return n

def Ejercicio8_RSA(mensaje,e,d,n):
    r=GenerarResumen(mensaje)
    print (r)
    r=msg2num(r)
    print (r)
    f=GenerarFirma(r,d,n)
    print (f)
    print ('A enviaria r y f')
    print ('B debe generar un nuevo resumen')
    print (' y con la publica de A genera un nuevo valor')
    if(VerificarFirma(mensaje,f,e,n)):
        print ('Todo en orden. Firma valida')
    else :
        print ('firma invalida')        
#Genero las llaves
public,private=genkeys(16)

#creo el mensaje
msg = bytearray(get_random_bytes())
#print (msg)
#print (public,private)
#print ("valor sha1")
#print (sha1(msg))
#print (msg2num(sha1(msg)))

e=public[1]
d=private[1]
n=public[0]
print (e ,d,n)
Ejercicio8_RSA(msg,e,d,n)



    
    
