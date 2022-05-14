from cmath import log
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy, scipy.optimize

# Ingreso de variables
t0 = float(input("Ingrese tiempo inicial: "))

# Cambiar ruta csv para abrir distintas mediciones
data = pd.read_csv(r'D:\Axel\UNTREF\Acústica 1\Mediciones\Mediciones forzadas con alem\medicion-2022Apr25-204950.csv', sep=';', header=None, usecols=[0,1,2])   #read the csv file (put 'r' before the path string to address any special characters in the path, such as '\'). Don't forget to put the file name at the end of the path + ".csv"
data = data.apply(lambda x: x.str.replace(',','.'))
tiempo = data[0].to_numpy(dtype=float)
aceleración1 = data[1].to_numpy(dtype=float)
aceleración2 = data[2].to_numpy(dtype=float)
A = np.amax(aceleración1)

# Limitar a t0 < t < t1
indext0 = tiempo.tolist().index(t0)
t1 = input("Ingrese tiempo final: ")
if t1 == True:
    t1 = float(t1)
    indext1 = tiempo.tolist().index(t1)
    tiempo = tiempo[indext0:indext1]
    aceleración1 = aceleración1[indext0:indext1]
    aceleración2 = aceleración2[indext0:indext1]
else:
    tiempo = tiempo[indext0:]
    aceleración1 = aceleración1[indext0:]
    aceleración2 = aceleración2[indext0:]

# Aproximar a un seno
def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
   
    ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(numpy.fft.fft(yy))
    guess_freq = abs(ff[numpy.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = numpy.std(yy) * 2.**0.5
    guess_offset = numpy.mean(yy)
    guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * numpy.sin(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*numpy.pi)
    fitfunc = lambda t: A * numpy.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}

aproximación1 = fit_sin(tiempo, aceleración1)
print("Valores aproximación senoidal acelerómetro 1:")
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, frequency=%(freq)s, period=%(period)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % aproximación1 )
aproximación2 = fit_sin(tiempo, aceleración2)
print("Valores aproximación senoidal acelerómetro 2:")
print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, frequency=%(freq)s, period=%(period)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % aproximación2 )


# Cálculo de transmisibilidad
Tf = 20*np.log10(abs(aceleración2)/abs(aceleración1))
Tf_fit = 20*np.log10(abs(aproximación2['amp'])/abs(aproximación1['amp']))
print("La transmisibilidad calculada con las aproximaciones es de " + str(Tf_fit) + "dB")

# Aproximar transmisibilidad a una recta
def linear(x, a, b):
	return a*x + b
constants = scipy.optimize.curve_fit(linear, tiempo, Tf)
a_fit = constants[0][0]
b_fit = constants[0][1]
fit = []
for i in tiempo:
	fit.append(linear(i, a_fit, b_fit))
print("La pendiente de la recta aproximada es: " + str(a_fit))
print("La ordenada de la recta aproximada es: " + str(b_fit))

# Ploteo
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('Oscilaciones forzadas')
ax1.plot(tiempo,aceleración1, color='r', label='Acelerómetro superior')
ax1.plot(tiempo, aproximación1["fitfunc"](tiempo), color='k', label="Sine fit acelerómetro superior")
ax1.plot(tiempo,aceleración2, color='b', label='Acelerómetro inferior')
ax1.plot(tiempo, aproximación2["fitfunc"](tiempo), color='y', label="Sine fit acelerómetro inferior")
ax2.plot(tiempo, Tf, '.', color='g', label="Scatter plot transmisibilidad")
ax2.plot(tiempo, fit, color='k', label="Linear fit transmisibilidad")
ax1.set_ylabel("Aceleración[g]")
ax2.set_ylabel("Transmisibilidad[dB]")
ax2.set_xlabel("Tiempo[s]")
ax1.set_xticks(np.linspace(t0,tiempo[-1],8))
ax2.set_xticks(np.linspace(t0,tiempo[-1],8))
ax1.set_yticks(np.linspace(-A,A,5))
ax1.legend()
ax2.legend()
ax1.grid()
ax2.grid()
plt.show()