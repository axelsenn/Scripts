from cmath import log, pi
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Ingreso de variables
t0 = float(input("Ingrese tiempo inicial: "))

# Ingresar ruta csv del archivo a analizar
data = pd.read_csv(r'D:\Axel\UNTREF\Acústica 1\Mediciones\Mediciones libres\Medición libre 1.csv', sep=';', header=None, usecols=[0,2])   #read the csv file (put 'r' before the path string to address any special characters in the path, such as '\'). Don't forget to put the file name at the end of the path + ".csv"
data = data.apply(lambda x: x.str.replace(',','.'))
tiempo = data[0].to_numpy(dtype=float)
aceleración = data[2].to_numpy(dtype=float)

# Limitar a tiempos > t0
indext = tiempo.tolist().index(t0)
print(indext)
tiempo = tiempo[indext:]
print(tiempo)
aceleración = aceleración[indext:]
print(aceleración)

# Calcular max y tmax medios
input_list = tiempo.tolist()
middle = float(len(input_list))/2
if middle % 2 != 0:
    middle = input_list[int(middle - .5)]
else:
    middle = input_list[int(middle)]
print("middle =" + str(middle))

index_middle = tiempo.tolist().index(middle)
print("index middle =" + str(index_middle))
print(aceleración[index_middle:])
max = np.amax(aceleración[index_middle:])
print("max =" + str(max))
index_max = aceleración[index_middle:].tolist().index(max)+index_middle
print("index max =" + str(index_max))
tmax = tiempo[index_max]
print("tmax =" + str(tmax))

# Cálculo de parametros de exponencial
A = np.amax(aceleración)
b = log(max/A)/(tmax-t0)
decaimiento = A*np.exp(b*(tiempo-t0))

# Cálculo de período
index_A = aceleración.tolist().index(A)
A2 = np.amax(aceleración[index_A+5:])
index_A2 = aceleración.tolist().index(A2)
t_A = tiempo[index_A]
t_A2 = tiempo[index_A2]
print("index A2 =" + str(index_A2))
print("A =" + str(A))
print("A2 =" + str(A2))
print("t_A =" + str(t_A))
print("t_A2 =" + str(t_A2))
Td = t_A2 - t_A
print("Td =" + str(Td))

# Cálculo de omega d
wd = (2*pi)/Td
print("wd =" + str(wd))

# Print de la función
print("y(t) ="+ str(round(A,3)) + "e^(" + str(b) + "t)")
print("")
print("b = " + str(b))
print("")
print("xi = " + str(abs(b)/wd))

# Ploteo
plt.plot(tiempo,aceleración, color='b', label='oscilación')
plt.plot(tiempo,decaimiento, '--', color='r', label='decaimiento')
plt.plot(tiempo,-decaimiento, '--', color='r')
plt.ylabel("Aceleración[g]")
plt.xlabel("Tiempo[s]")
plt.xticks(np.linspace(t0,tiempo[-1],8))
plt.yticks(np.linspace(-A,A,5))
plt.legend()
plt.grid()
plt.show()

