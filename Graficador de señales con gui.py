from numpy import cos, sin, arange, pi
import matplotlib.pyplot as plt
import PySimpleGUI as sg

# Define the window's contents
layout = [[sg.Text("w = (a/b)*π \n")], [sg.Text("Ingrese función(cos o sin)")],
          [sg.Input(key='-INPUT0-')],[sg.Text("Ingrese a")],
          [sg.Input(key='-INPUT1-')], [sg.Text("Ingrese b")],
          [sg.Input(key='-INPUT2-')], [sg.Text("Multiplicar por π?")],
          [sg.Input(key='-INPUT3-')], [sg.Text("Ingrese el rango a graficar")],
          [sg.Input(key='-INPUT4-')],
          [sg.Text(size=(40,1), key='-OUTPUTw-')],
          [sg.Text(size=(40,1), key='-OUTPUTx-')],
          [sg.Button('Ok'), sg.Button('Quit')]]

# Create the window
window = sg.Window('Calculadora de funciones discretas', layout)

# Display and interact with the Window using Event
while True:
    event, values = window.read()
    func = values['-INPUT0-']
    a = float(values['-INPUT1-'])
    b = float(values['-INPUT2-'])
    c = str(values['-INPUT3-'])
    L = float(values['-INPUT4-'])

    if c == "y" or c == "yes" or c == "si" or c == "s":
        c = pi
    elif c == "n" or c == "no":
        c = 1

    if a % 1 == 0:
        round_a = round(a)
    else: round_a = round(a,2)

    if b % 1 == 0:
        round_b = round(b)
    else: round_b = round(b,2)

    # Calcular omega
    w = (a/b)*c

    if func == "c":
        func = "cos"
    elif func == "s":
        func = "sin"
        
    # Definir función
    n = arange(-L, L+1, 1)
    if func == "cos":
        x = cos(w*n)
    elif func == "sin":
        x = sin(w*n)

    if event == sg.WINDOW_CLOSED or event == 'Quit':
            break
    # Output a message to the window
    if c == pi:
        window['-OUTPUTw-'].update("w = " + str(round_a) + "π" + "/" + str(round_b), text_color = 'yellow')
        window['-OUTPUTx-'].update("x[n] = " + str(func) + "(" + str(round_a) + "π" + "n" + "/" + str(round_b) + ")", text_color = 'yellow')
    elif c == 1:
        window['-OUTPUTw-'].update("w = " + str(round_a) + "/" + str(round_b), text_color = 'yellow')
        window['-OUTPUTx-'].update("x[n] = " + str(func) + "(" + str(round_a) + "n" + "/" + str(round_b) + ")", text_color = 'yellow')

    # Graficar función
    plt.stem(n, x)
    plt.xlabel('n')
    plt.ylabel('x [n]')
    plt.xticks(n)
    plt.grid()
    plt.show()


# Finish up by removing from the screen
window.close()

