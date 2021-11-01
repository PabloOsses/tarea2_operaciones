import random
from math import e as euler

def distancia(sol, inicio, fin):
    """Esta funcion solo calcula las distancias entre puestos y es 
    utilizada en la funcion siguiente llamada esfuerzo
    @param sol: es la solucion a evaluar en la funcion, es una matriz con el numero del puesto y el largo del puesto
    @param inicio: es un numero que determina desde que puesto de comienza a calcular la distancia 
    @param fin:es un numero que determina en que puesto se termina de calcular la distancia
    @return total: retorna la distancia entre dos puestos """
    total=0
    suma=0
    xi=sol[inicio][1]/2
    xj=sol[fin][1]/2
    if (fin-inicio)>1:
        for i in range(inicio+1,fin):
            suma+=sol[i][1]
            
    total=xi+suma+xj
    return total

def esfuerzo(sol, w):
    """esta es la funcion objetivo del simulated annealing, 
     @param sol: es la solucion a evaluar en la funcion, es una matriz con el numero del puesto y el largo del puesto
     @param w: es una matriz con las variables wij del problema
     @return total: retorna el total de la funcion de esfuerzo
    """
    total=0
    dist=0
    for i in range(0,len(sol)-1):
        for j in range(1,len(sol)):
            dist=distancia(sol,i,j)
            #print(w[i][j])
            total+= w[i][j]*dist
    return total


def sol_aleatoria(solucion,n):
    """
    Esta funcion genera una solucion aleatoria
    @param solucion: solucion base desde la cual se genera una solucion aleatoria, es una matriz con el numero del puesto y el largo del puesto
    @param n: largo de la solucion aleatoria
    @return solucion_random : solucion aleatoria 
    """
    solucion_random=list(solucion)
    largo_s_random=1.0/(float(n))
    aux=list()
    #se generan dos numeros flotantes aleatorios entre 0 y 1
    numero_aleatorio=round(random.random(),2)
    numero_aleatorio2=round(random.random(),2)
    
    for i in range(0,n):
        if ((i*largo_s_random)<numero_aleatorio) and (((i+1)*largo_s_random)>=numero_aleatorio):
            aux=solucion_random[i]
            
            for j in range(0,n):
                if ((j*largo_s_random)<numero_aleatorio2) and (((j+1)*largo_s_random)>=numero_aleatorio2):
                    solucion_random[i]=solucion_random[j]
                    solucion_random[j]=aux
    return solucion_random


#primero se leen e inicilizan los datos
file = open("QAP_sko56_04_n", "r")
n=0
largos=list() #variables l (largos) de los puestos
w=list() #variable w de la tarea
for i,line in enumerate(file):
    if i==0:
        #primera linea del archivo
        n=int(line.split("\n")[0])
    elif i==1:
        #segunda linea del archivo
        largos=line.split("\n")[0].split(",")
        largos = [int(x) for x in largos]
        #la ultima linea es para convertir string a int
    else:
        #siguientes lineas del archivo
        w.append(line.split("\n")[0].split(","))
        for x in range(0, len(w)):
            for y in range(0, len(w[x])):
                w[x][y] = int(w[x][y])
file.close()
#fin inicializacion de datos

#implementacion de solucion simulated annealing
puestos=list(range(1, n+1)) 
solucion=list() #solucion inicial, es una matriz con el numero del puesto y el largo del puesto
for i in range(0,n):
    solucion.append([puestos[i],largos[i]])

print("SOLUCION INICIAL")
#print(solucion)
print("\n")
print("ESFUERZO  INICIAL")
print(esfuerzo(solucion,w))
print("\n")
#generar solucion aleatoria

t0=50.0 #temperatura inicial
alfa=0.4 #enfriamiento
tmin=0.2 #temperatura minima
n_iteracion=1
while t0>tmin:
    print(f"------iteracion: {n_iteracion}-------")
    n_iteracion+=1
    #se genera solucion aleatoria
    solucion_potencial=sol_aleatoria(solucion,n)
    #diferencia de funciones objetivo
    dif_esfuerzos=esfuerzo(solucion_potencial,w)-esfuerzo(solucion,w)
    print(f"DIFERENCIA es: {dif_esfuerzos}")
    if dif_esfuerzos<0:
        print("--EXPLOTACION")
        solucion=list(solucion_potencial)
    else:
        probabilidad= euler**((-1*dif_esfuerzos)/t0)
        print("--Calcular probabilidad ")
        print(f"Probabilidiad de aceptacion: {probabilidad}")
        if round(random.random(),2)< probabilidad:
            print("--EXPLORACION")
            solucion=list(solucion_potencial) 
    t0=alfa*t0
print("RESULTADO FINAL")
#print(solucion)

print("ESFUERZO  FINAL")
print(esfuerzo(solucion,w))