import RPi.GPIO as GPIO
import time
from telnetlib import Telnet
import random

#Diccionadio de configuraciones de presets
Configurations={"Cam2Gral":1,"Cam1Gral":2,"Cam1Izq":5,"Cam1Cnt":4,"Cam1Der":3,"Cam1S1":6,"Cam1S2":7,"Cam1S3":8,"Cam1S4":9,"Cam1S5":10,"Cam1S6":11,"Cam1S7":12}

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

def determinarConfiguracion(cadena):
	if cadena=="1000000":
    	conf="Cam1S1"
    	id_preset=Configurations[conf]

    if cadena=="0100000":
    	conf="Cam1S2"
		id_preset=Configurations[conf]
		            
   	if cadena=="0010000":
   		conf="Cam1S3"
   		id_preset=Configurations[conf]
		            
   	if cadena=="0001000":
   		conf="Cam1S4"
   		id_preset=Configurations[conf]
		            
   	if cadena=="0000100":
   		conf="Cam1S5"
   		id_preset=Configurations[conf]
		            
   	if cadena=="0000010":
   		conf="Cam1S6"
   		id_preset=Configurations[conf]

   	if cadena=="0000001":
   		conf="Cam1S7"
   		id_preset=Configurations[conf]
   	return id_preset

def activarPreset(id_preset):
	telnet.write('xCommand Camera Preset Activate PresetId:'+str(id_preset)+'\n')
    telnet.read_until('OK')

def determinarZona(cadena):
	if cadena== "1000000" or cadena== "0100000" or cadena== "1100000":
    	conf="Cam1Izq"
    	id_preset=Configurations[conf]        

    elif cadena== "0010000" or cadena== "0001000" or cadena== "0000100" or cadena== "0011000" or cadena== "0001100"or cadena== "0011100":
    	conf="Cam1Cnt"
    	id_preset=Configurations[conf]        

    elif cadena== "0000001" or cadena== "0000010" or cadena== "0000011":
    	conf="Cam1Der"
    	id_preset=Configurations[conf]
    	
    return id_preset


#Configuracion de puertos de recepcion de sennal en placa de la barra de sensores

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

#Conexion al codec sx80
telnet = Telnet('10.7.100.3', 23)
telnet.read_until('login:')
telnet.write('admin\n')
telnet.read_until('Password:')
telnet.write('ccafvc.\n')
telnet.read_until('OK')

#Wake up camara, si la camara se encuentra en standby
telnet.write('xCommand Standby Deactivate\n')
telnet.read_until('OK')
time.sleep(1)

#Envio del preset 1 para ajustar la camara 2 antes de iniciar el tracking
telnet.write('xCommand Camera Preset Activate PresetId:1\n')
telnet.read_until('OK')
time.sleep(0.2)
telnet.write('xCommand Camera Preset Activate PresetId:2\n')
telnet.read_until('OK')
time.sleep(0.2)

#Definicion de estructura para guardar las snneales en el tiempo
States={"actual":"0000000","pasado":"0000000","antepasado":"0000000"}

#Se definen variables iniciales para empezar desde planos generales
cadena_inicial="0000000"
id_inicial=2
id_preset=2
flag=True
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

    if contarOnes(States["actual"])>3:
    	id_preset=2

    else:
	    if States["actual"]!="0000000":
	    	if contarOnes(States["actual"])==1:
	    		if States["pasado"]==States["actual"] or States["pasado"]=="0000000":
	    			id_preset=determinarConfiguracion(States["actual"])
	    		else:
	    			id_preset=determinarZona(States["actual"])
	    	else:
	    		id_preset=determinarZona(States["actual"])
	    else:
	    	pass

    if id_inicial!=id_preset:
    	activarPreset(id_preset)
    	id_inicial=id_preset

    #Se hace una pausa
	time.sleep(0.3)
	#Se enciende el led
	GPIO.output(23,0)
	#Se hace otra pausa
	time.sleep(0.2)

	#Se lee la sennal de los sensores
	cadena_inicial=str(S1)+str(S2)+str(S3)+str(S4)+str(S5)+str(S6)+str(S7)



    			
