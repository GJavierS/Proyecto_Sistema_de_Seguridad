from tkinter import *
import time 
import serial
import smtplib
from email.message import EmailMessage
import threading

Arduino = serial.Serial('COM5', 9600)
time.sleep(0.5)


def EnviarCorreo():
	#Declaro el correo y contraseña
    Emisor = "luisalbertodejesusv883@gmail.com"
    Contrasena = "qfurqdaeaamepcer"
    Receptor = "t1013600621@unitru.edu.pe"

    print("Iniciando envio")
    #Obteniendo la fecha y hora actual 
    Fecha = time.strftime("%d/%m/%y")
    Hora = time.strftime("%H:%M:%S")

    #Titulo del correo
    Asunto = "ALERTA DE SEGURIDAD"

    #Creando el mensaje que se quiere mandar
    Mensaje = "Alguien abrio la puerta el "+ Fecha + " a la hora " + Hora

    #Aspectos de mensaje
    em = EmailMessage()
    em["From"] = Emisor
    em["To"] = Receptor
    em["Subject"] = Asunto
    em.set_content(Mensaje)

    #Preparando el envio
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(Emisor, Contrasena)
        smtp.sendmail(Emisor, Receptor, em.as_string())

cont = 0

def llamar_sistema():
    global cont
    while True:
        time.sleep(1)
        val = Arduino.readline()
        val = val.decode()
        #Para ver los datos que arroja
        a = int(val)
        print(a)
        if (a == 0):
            cont =+1
            if (cont <= 1):
                EnviarCorreo()
                print('ALERTA')
        elif (a == 1):
            cont = 0

def encender():
    Arduino.write('a'.encode())
    time.sleep(0.1)

def apagar():
    Arduino.write('b'.encode())
    time.sleep(0.1)


def cerrarInterfaz():
    Arduino.close()
    control.destroy()


threading.Thread(target=llamar_sistema).start()

control = Tk()

control.geometry("500x200")
control.title('control de sistema')

titleFrame = Frame()
titleFrame.config(bg = "yellow", width = "500", height = "80")
titleFrame.place(x=0, y=0)
#titulo
lbltitulo = Label(titleFrame, text = "ENCENDIDO Y APAGADO DE SISTEMA", bg = "yellow", font =("ARIAL", 15))
lbltitulo.place(x=70, y=20)

botonesFrame = Frame()
botonesFrame.config(bg = "orange", width = "500", height = "120")
botonesFrame.place(x=0, y=80)

#boton de encender
encender_c = Button(botonesFrame, text = "ACTIVAR", bg = "green", fg = "white", font = ("ARIAL", 12),command = lambda:encender())
encender_c.place(x=100, y=40)

#boton de apagar
apagar_c = Button(botonesFrame, text = "APAGAR", bg = "red", fg = "white", font = ("ARIAL", 12),command = lambda:apagar())
apagar_c.place(x=300, y=40)

#boton de Cerrar sistema
cerrar= Button(botonesFrame, text = ("Salir"),font = ("ARIAL", 14), command = lambda:cerrarInterfaz())
cerrar.place(x=440, y=80)


control.mainloop()
