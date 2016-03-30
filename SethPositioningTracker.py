import RPi.GPIO as GPIO
import time
from telnetlib import Telnet
import random

# Indice de configuraciones versus cadena
Indice={"0000000":"Cam1Gral",
		"0000000":"Cam2Gral",
		"1000000":"Cam1C1S1",
		"0100000":"Cam1C1S2",
		"0010000":"Cam1C1S3",
		"0001000":"Cam1C1S4",
		"0000100":"Cam1C1S5",
		"0000010":"Cam1C1S6",
		"0000001":"Cam1C1S7",
		"1100000":"Cam1C2S1",
		"0110000":"Cam1C2S2",
		"0011000":"Cam1C2S3",
		"0001100":"Cam1C2S4",
		"0000110":"Cam1C2S5",
		"0000011":"Cam1C2S6",
		"1110000":"Cam1C3S1",
		"0111000":"Cam1C3S2",
		"0011100":"Cam1C3S3",
		"0001110":"Cam1C3S4",
		"0000111":"Cam1C3S5",
		"1111000":"Cam1C4S1",
		"0111100":"Cam1C4S2",
		"0011110":"Cam1C4S3",
		"0001111":"Cam1C4S4",
		"1111100":"Cam1C5S1",
		"0111110":"Cam1C5S2",
		"0011111":"Cam1C5S3",
		"1111110":"Cam1C6S1",
		"0111111":"Cam1C6S2",
		"1111111":"Cam1C7S1",
		}

#Diccionario de configuraciones para SX80
Configuraciones={"Cam1Gral":(z,p,t),
				"Cam2Gral":(z,p,t),
				"Cam1C1S1":(z,p,t),
				"Cam1C1S2":(z,p,t),
				"Cam1C1S3":(z,p,t),
				"Cam1C1S4":(z,p,t),
				"Cam1C1S5":(z,p,t),
				"Cam1C1S6":(z,p,t),
				"Cam1C1S7":(z,p,t),
				"Cam1C2S1":(z,p,t),
				"Cam1C2S2":(z,p,t),
				"Cam1C2S3":(z,p,t),
				"Cam1C2S4":(z,p,t),
				"Cam1C2S5":(z,p,t),
				"Cam1C2S6":(z,p,t),
				"Cam1C3S1":(z,p,t),
				"Cam1C3S2":(z,p,t),
				"Cam1C3S3":(z,p,t),
				"Cam1C3S4":(z,p,t),
				"Cam1C3S5":(z,p,t),
				"Cam1C4S1":(z,p,t),
				"Cam1C4S2":(z,p,t),
				"Cam1C4S3":(z,p,t),
				"Cam1C4S4":(z,p,t),
				"Cam1C5S1":(z,p,t),
				"Cam1C5S2":(z,p,t),
				"Cam1C5S3":(z,p,t),
				"Cam1C6S1":(z,p,t),
				"Cam1C6S2":(z,p,t),
				"Cam1C7S1":(z,p,t),
				}

#funcion que realiza el HTTP post al codec

#Por terminar
def postorder(z,p,t):
	return True


#Funcion que al recibir la cadena, entrega la cantidad de ceros antes del primer 1
def contarZeros(cadena):
	countZero=0
	flag=True
	for elemento in cadena:
		if flag:
			if elemento=='0':
				countZero+=1
			else:
				flag=False
	return countZero

#Funcion que al recibir la cadena, entrega la cantidad de ceros antes del primer 1 pero de atras hacia adelante
def contarZerosReverse(cadena):
	cadena=cadena[::-1]
	countZero=0
	flag=True
	for elemento in cadena:
		if flag:
			if elemento=='0':
				countZero+=1
			else:
				flag=False
	return countZero

#funcion que entrega cuantos caracteres hay entre el primer y ultimo 1 de la cadena
def contarOnes(cadena):
	if contarZeros(cadena)==7:
		return 0
	return 7 - (contarZeros(cadena)+contarZerosReverse(cadena))

#Funcion que entrega la cadena en el formato correcto, sin ceros entre el primer y ultimo 1
def transformarCadena(cadena):
	cadenaDefinitiva=''
	if contarZeros(cadena)==7:
		return '0000000'
	elif contarZeros(cadena)==0 and contarZerosReverse==0:
		return '1111111'
	else:
		cadenaDefinitiva='0'*contarZeros(cadena)+'1'*contarOnes(cadena)+'0'*contarZerosReverse(cadena)
		return cadenaDefinitiva

#Configuracion de puertos de recepcion de señal en placa de la barra de sensores

#Definicion de pines de la GPIO
Sen_1=26
Sen_2=19
Sen_3=13
Sen_4=21
Sen_5=20
Sen_6=16
Sen_7=12

#Declaracion de tipos de pin (entrada o salida)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Sen_1,GPIO.IN)
GPIO.setup(Sen_2,GPIO.IN)
GPIO.setup(Sen_3,GPIO.IN)
GPIO.setup(Sen_4,GPIO.IN)
GPIO.setup(Sen_5,GPIO.IN)
GPIO.setup(Sen_6,GPIO.IN)
GPIO.setup(Sen_7,GPIO.IN)
GPIO.setup(23,GPIO.OUT)


#Definicion de estructura para guardar las señales en el tiempo
States={"actual":"00000000","pasado":"00000000","antepasado":"00000000"}

#Se definen variables iniciales para empezar desde planos generales
cadena_inicial="0000000"
id_inicial=2

#Inicio de loop
while (True):
	#Lectura de sennales
	GPIO.output(23,1)
    S1=GPIO.input(Sen_1)
    S2=GPIO.input(Sen_2)
    S3=GPIO.input(Sen_3)
    S4=GPIO.input(Sen_4)
    S5=GPIO.input(Sen_5)
    S6=GPIO.input(Sen_6)
    S7=GPIO.input(Sen_7)

   	#Actualizacion de estados 
    States["antepasado"]=States["pasado"]
    States["pasado"]=States["actual"]
    States["actual"]=cadena_inicial

	Velocidad=8

	ZPTpasado=Configuraciones[Indice[States["pasado"]]]
	ZPTactual=Configuraciones[Indices[States["actual"]]]
	delta=ZPTpasado-ZPTactual

	#inicializacion de posicion de la camara
	position=ZPTpasado

	while position<=ZPTactual:




