# -*- coding: utf-8 -*-
"""
Created on Apr 7 15:04:21 2014
Python 2.7.3
@author: Jose Arcos Aneas
@DNI:74740565-H
@Asignatura: Criptografia
"""

from collections import deque
from operator import xor  

print "*"*30
print "Practica 2 Criptografia. Cifrado de flujo"
print "*"*30


"""
Funcion para mostrar un polinomio 

Utilizada en el algoritmo de Berlekamp_Massey
"""
def poly(polinomio):
    resul = ''
    lista = sorted(polinomio, reverse=True)
    for i in lista:
        if i == 0:
            resul += '1'
        else:
            resul += 'x^%s' % str(i)
        if i != lista[-1]:
            resul += ' + '
    return resul


"""
Funcion que calcula la distancia de Hamming entre dos listas
"""
def distancia_hamming(s1,s2):
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))
"""
funcion para comprobar si una secuencia de bits cumple los postulados
de Golomb
"""
def Golomb(lista):

    if abs(lista.count(1) - lista.count(0) ) <= 1: 
        print "Cumple el postulado 1 de Golomb" 
    else: 
        print "No Cumple el postulado 1 de Golomb"

    # Segundo Postulado
    # Buscamos las rachas haciendo el el primer 
    # y el ultimo bits sean diferentes 
    longitud = len(lista)
    veces = 0
    while lista[0] == lista[-1] and veces != longitud:
        lista = lista[1:] + lista[0:1]
        veces +=1  
    cont = 1
    rachas = {} 
    # Recorremos todo el periodo
    # y anotamos el tamaño de las rachas 
    for i in range(longitud-1):
        if lista[i] == lista[i+1]:
            cont+=1
        else:
            try:
                rachas[cont]+=1
            except KeyError:
                rachas.update({cont: 1})
            cont = 1
        if longitud == i+2: 
            try:
               rachas[cont]+=1
            except KeyError:
               rachas.update({cont: 1}) 
    k_max = max(rachas.keys())
 
    try:
        # Si Hay 1 racha de longitud k y 1 racha de lontigud k-1
        postulado2 = (rachas[k_max] == 1) and (rachas[k_max-1] == 1) 
        # Comprobar 1 racha longitud k_max-1
        # 2 rachas longitud k_max-2
        # 4 rachas longitud k_max-3...
        for k in range(k_max-1,1,-1): 
            # Empieza en k_max-1
            if rachas[k] != rachas[k-1]>>1:
                postulado2 = False
                break
    except KeyError:
        postulado2 = False
    if postulado2 == True:
        print "Cumple el postulado 2 de Golomb"
    else:
        print "No Cumple el postulado 2 de Golomb" 
    # Tercer Postulado
    # Rotamos una posicion y calculamos la distancia de hamming 
    # con la original. Si se cumple seguimos rotando y comparando 
    # Si la distancia de Hamming no se ha cumplido en alguna comparacion
    # no se cumple el tercer postulado
    desplazada = deque(lista)
    desplazada.rotate(1)
    dist = distancia_hamming(lista, desplazada)
    postulado3 = True
    veces = 1
    while veces < longitud-1:
        # Rota una posición 
        desplazada.rotate(1)
        veces+=1
        sig_dist = distancia_hamming(lista, desplazada) 
        if dist != sig_dist : 
            postulado3 = False
            break
  
    if postulado3 == True:
        print "Cumple el postulado 3 de Golomb"
    else:
        print "No Cumple el postulado 3 de Golomb" 
# Ejecucion del Primer Ejercicio
print 'Ejercicio 1'
lista=[1,1,1,0,0,0,0,1,0,1,0,1,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1]
print "La lista: ",lista
Golomb(lista)
print "*"*30
"""
LFSR-Lineal Feedback shift register
Entrada: coeficientes, semilla,longitud
Salida:  Secuencia generada
Para todo el tamaño de la cadena a generar recorremos cada coeficiente
hacemo and y un xor con el anterior (primera iteraccion 0)
Añadimos la semilla a lista, se añade al pricipio y se desplaza la semilla
"""
def LFSR(coeficientes,semilla,longitud):    
    lista = []   
    for k in xrange(0,longitud):
        aux = 0
        for i in xrange(0,len(coeficientes)):           
            a = semilla[i]*coeficientes[i]
            aux = xor(aux,a)
        lista.append(int(semilla[len(semilla)-1]))
        semilla = [aux] + semilla
        semilla = semilla[0:len(semilla)-1] 
    return lista
    
p1=[1,0,0,1]
s1=[1,1,0,1]
k1=15
lfsr=LFSR(p1,s1,k1)
print "Ejercicio 2. "
print lfsr
print "*"*30

"""
NLFSR-Non Lineal Feedback shift register
Entrada:monomios, semilla,longitud
Salida:  Secuencia generada

"""
def NLFSR(monomios, semilla, k):
    lista = []       
    for _ in range(0,k): 
        aux = 0
        for monomio in monomios:
            r = 1
            for j,sem in zip(monomio,semilla):
                r = (r+sem*j)%2
            aux = xor(aux,r)        
        lista.append(aux)
        semilla = [aux]+semilla
        semilla = semilla[0:len(semilla)-1]
    return lista
    
print "Ejercicio 3."
nlfsr=NLFSR([[0,0,0,0],[1,1,1,0]],[1,1,0,1],20)
print nlfsr
print "*"*30


"""
Generador de Geffe
Esta funcion hace uso de la funcion LFSR.
Calcula las tres listas a partir de los LFSR y 
con los resultados aplicamos las operacion and
y sobre estos mismos resultados los xor correspondientes
Entrada 3 listas con los coeficientes de polinomios para los LFSR
3 secuencias que seran las semillas para cada uno de ellos 
y un numero k que sera la longitud
"""

def Geffe(p1,p2,p3,s1,s2,s3,k):
    l1 = LFSR(p1,s1,k)    
    l2 = LFSR(p2,s2,k)
    l3 = LFSR(p3,s3,k)
    lista = []  
    for i,j,k in zip(l1,l2,l3):
        x1 = i*j; x2= j*k; x3 = k;
        f = xor(xor(x1,x2),x3)
        lista.append(f)
    return lista
# Ejecucion del Ejercicio 4
p1=[1,0,0,1]
s1=[1,1,0,1]
p2=[1,0,0,1]
s2=[0,0,1,0]
p3=[1,0,1,0]
s3=[0,1,1,0]
k1=15

print 'Ejercicio 4'
resultado=Geffe(p1,p2,p3,s1,s2,s3,k1)
print resultado
print "-"*30
"""
Funcion para encriptar un texto a partir del generador de Geffe
"""
def Geffe_En(txt,p1,p2,p3,s1,s2,s3,k):
    result_l = Geffe(p1,p2,p3,s1,s2,s3,k)
    msg_lista = []
    for i,j in zip(txt,result_l):
        msg = xor(int(i),j)
        msg_lista.append(msg)        
    return msg_lista
texto=[1,0,0,0,1,1,0,1,0,0,1,1,1,1]
print "Geffe cifrado. Ejecutando ejemplo."
print "El texto a cifrar es: ",  str(texto)
print "El resultado es :"
en=Geffe_En(texto,p1,p2,p3,s1,s2,s3,k1)
print en
print "-"*30
"""
Funcion para desencriptar un texto (previamente encriptado)
Esta funcion utiliza el generador de Geffe, empleo 
la salida del ejercicio anterior como entrada este 
"""
def Geffe_Des(texto,p1,p2,p3,s1,s2,s3,k):
    result_l=Geffe(p1,p2,p3,s1,s2,s3,k)
    msg_des=[]
    for i,j in zip(texto,result_l):
        msg=xor(int(i),int(j))
        msg_des.append(msg)
    return msg_des


print "Geffe descifrado."
des=Geffe_Des(en,p1,p2,p3,s1,s2,s3,k1)
print "El resultado del descifrado es:",des
print "*"*30

"""
Algoritmo de Berlekamp_Massey
Toma como entrada una secuencia de 1's y 0's y determina 
el polinomio que genera la cadena y su complejidad
"""
def Berlekamp_Massey(secuencia):
    N = len(secuencia)
    s = secuencia[:]
    # Buscamos el primer entero tal que Sk =1
    for k in range(N):
        if s[k] == 1:
            break
    f = set([k + 1, 0]) 
    l = k + 1
    g = set([0])
    a = k
    b = 0
    r = k+1
    for n in range(r, N):
        d = 0
        for elemento in f:
            d ^= s[elemento + n - l]
        if d == 0:
            b += 1
        else:
            if 2 * l > n:
                f ^= set([a - b + elemento for elemento in g])
                b += 1
            else:
                aux = f.copy()
                f = set([b - a + elemento for elemento in f]) ^ g
                l = n + 1 - l
                g = aux
                a = b
                b = n - l + 1
    return poly(f), l


secuencia = (1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1)
polinomio, complejidad = Berlekamp_Massey(secuencia)
print "Ejercicio 5"
print "La secuencia es ", secuencia
print "El polinomio es:",  polinomio
print 'y la complejidad: ',  complejidad