#PABLO OSSES
#ROBERTO ISLA
#JORGE CONTRERAS
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
        #CASO EN EL QUE HAY PUESTOS ENTREMEDIO DE DOS PUESTOS
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
            
            total+= w[sol[i][0]-1][sol[j][0]-1]*dist
            #print(f" {i},{j}: puestos: {sol[i][0]},{sol[j][0]} dist {dist}, wij: {w[sol[i][0]-1][sol[j][0]-1]},")

    return total

def sol_aleatoria_swap(solucion,n):
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

def imprime_puestos(sol):
    """
    las variables de solucion trabajadas en simulated annealing y las funciones 
    de esfuerzo y distancia, son matrices con el numero de puesto y la distancia 
    imprime_puestos solo imprime los puestos de una solucion
    @param sol: con el numero de puesto y la distancia 
    @return orden_puestos: retorna solo los puestos de una solucion 
    """ 
    orden_puestos=list()
    for j in range(0,len(sol)):
        orden_puestos.append(sol[j][0])
    return orden_puestos

"""
INICIALIZACION DE DATOS
"""
file = open("QAP_sko56_04_n", "r")
n=0 #cantidad de puestos
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
        #siguientes lineas del archivo, matriz w
        w.append(line.split("\n")[0].split(","))
        for x in range(0, len(w)):
            for y in range(0, len(w[x])):
                w[x][y] = int(w[x][y])
file.close()

"""
FIN INICIALIZACION DE DATOS
"""
"""
INICIO IMPLEMENTACION SIMULATED ANNEALING
"""
puestos=list(range(1, n+1)) 
solucion=list() 
#solucion, es una matriz con el numero del puesto y el largo del puesto
for i in range(0,n):
    solucion.append([puestos[i],largos[i]])


"""
Hasta ahora la solucion inicial es sigue el orden normal
esto es puesto 1,2,3,4,5...
la funcion shuffle de la libreria random toma esta solucion inicial y
la reordena de forma aleatoria, para crear una solucion inicial aleatoria uniforme.
"""
random.shuffle(solucion)

print("SOLUCION INICIAL")
print(imprime_puestos(solucion))

print("ESFUERZO  INICIAL")
print(esfuerzo(solucion,w))
print("\n")
#generar solucion aleatoria

t_inicial=4000.0 #temperatura inicial
alfa=0.98 #enfriamiento
t_min=400 #temperatura minima
n_iteracion=1
aceptado=0
no_aceptado=0
while (t_inicial>t_min) :
    
    #se genera solucion aleatoria
    solucion_potencial=sol_aleatoria_swap(solucion,n)
    #diferencia de funciones objetivo
    dif_esfuerzos=esfuerzo(solucion_potencial,w)-esfuerzo(solucion,w)
    
    if dif_esfuerzos<0:
        #EXPLORACION DEL ALGORITMO
        solucion=list(solucion_potencial)
        print(f"{n_iteracion}: EXPLOTACION, diferencia: {dif_esfuerzos}, temperatura: {t_inicial} , esfuerzo: {esfuerzo(solucion,w)}")
    else:
        probabilidad= euler**((-1*dif_esfuerzos)/t_inicial)
        #PROBABILIDAD PARA EL CRITERIO DE METROPOLI
        
        numero_random=round(random.random(),5)
        if numero_random< probabilidad:
            #EXPLOTACION DEL ALGORITMO
            solucion=list(solucion_potencial) 
            print(f"{n_iteracion}: EXPLORACION, PROB:{probabilidad}--numero: {numero_random}, temp: {t_inicial}, dif: {dif_esfuerzos}, esfuerzo: {esfuerzo(solucion,w)}")
            aceptado+=1
        else:
            #NO ACEPTA LA SOLUCION
            print(f"{n_iteracion}: NO ACEPTA, PROB:{probabilidad}--numero: {numero_random}, temp: {t_inicial} dif: {dif_esfuerzos}, esfuerzo: {esfuerzo(solucion_potencial,w)}")
            no_aceptado+=1
    t_inicial=round(alfa*t_inicial,2)
    #ENFRIAMIENTO
    n_iteracion+=1
print("SOLUCION FINAL")
print(imprime_puestos(solucion))

print("ESFUERZO  FINAL")
print(esfuerzo(solucion,w))

print(f"EXPLOTACIONES {114-aceptado-no_aceptado}, EXPLORACIONES {aceptado}, NO ACEPTADO {no_aceptado}")