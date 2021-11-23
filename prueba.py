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
        for j in range(i+1,len(sol)):
            dist=distancia(sol,i,j)
            #print(w[i][j])
            total+= w[sol[i][0]-1][sol[j][0]-1]*dist
            print(f" {i},{j}: puestos: {sol[i][0]},{sol[j][0]} dist {dist}, wij: {w[sol[i][0]-1][sol[j][0]-1]},")

    return total


def sol_aleatoria_swap(solucion,n):
    """
    Esta funcion genera una solucion aleatoria, mediante el swap de dos posiciones
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

def imprime_puestos(sol):
    orden_puestos=list()
    for j in range(0,len(sol)):
        orden_puestos.append(sol[j][0])
    return orden_puestos

#primero se leen e inicilizan los datos
file = open("S8", "r")
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

print(w)


