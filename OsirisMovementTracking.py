import RPi.GPIO as GPIO
import time
from telnetlib import Telnet
import random


Configurations={"Cam2Gral":1,"Cam1Gral":2,"Cam1Izq":3,"Cam1Cnt":4,"Cam1Der":5,"Cam1S1":6,"Cam1S2":7,"Cam1S3":8,"Cam1S4":9,"Cam1S5":10,"Cam1S6":11,"Cam1S7":12}

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

def contarOnes(cadena):
	if contarZeros(cadena)==7:
		return 0
	return 7 - (contarZeros(cadena)+contarZerosReverse(cadena))

def transformarCadena(cadena):
	cadenaDefinitiva=''
	if contarZeros(cadena)==7:
		return '0000000'
	elif contarZeros(cadena)==0 and contarZerosReverse==0:
		return '1111111'
	else:
		cadenaDefinitiva='0'*contarZeros(cadena)+'1'*contarOnes(cadena)+'0'*contarZerosReverse(cadena)
		return cadenaDefinitiva

Sen_1=26
Sen_2=19
Sen_3=13
Sen_4=21
Sen_5=20
Sen_6=16
Sen_7=12

GPIO.setmode(GPIO.BCM)
GPIO.setup(Sen_1,GPIO.IN)
GPIO.setup(Sen_2,GPIO.IN)
GPIO.setup(Sen_3,GPIO.IN)
GPIO.setup(Sen_4,GPIO.IN)
GPIO.setup(Sen_5,GPIO.IN)
GPIO.setup(Sen_6,GPIO.IN)
GPIO.setup(Sen_7,GPIO.IN)
GPIO.setup(23,GPIO.OUT)


#conexion
telnet = Telnet('10.7.100.4', 23)
telnet.read_until('login:')
telnet.write('admin\n')
telnet.read_until('Password:')
telnet.write('\n')
telnet.read_until('OK')

#wake up camara
telnet.write('xCommand Standby Deactivate\n')
telnet.read_until('OK')
time.sleep(1)


telnet.write('xCommand Camera Preset Activate PresetId:1\n')
telnet.read_until('OK')
time.sleep(0.2)


States={"actual":"0000000","pasado":"0000000","antepasado":"0000000"}

cadena_inicial="0000000"

while (True):
	GPIO.output(23,1)
    S1=GPIO.input(Sen_1)
    S2=GPIO.input(Sen_2)
    S3=GPIO.input(Sen_3)
    S4=GPIO.input(Sen_4)
    S5=GPIO.input(Sen_5)
    S6=GPIO.input(Sen_6)
    S7=GPIO.input(Sen_7)

    
    States["antepasado"]=States["pasado"]
    States["pasado"]=States["actual"]
    States["actual"]=cadena_inicial


    if contarOnes(cadena_inicial)>3:
    	conf="Cam1Gral"
    	id1=Configurations[conf]

    elif States["actual"]== "1000000" or States["actual"]== "0100000" or States["actual"]== "1100000":
    	conf="Cam1Izq"
    	id1=Configurations[conf]

    elif States["actual"]== "0010000" or States["actual"]== "0001000" or States["actual"]== "0000100" or States["actual"]== "0011000" or States["actual"]== "0001100"or States["actual"]== "0011100":
    	conf="Cam1Cnt"
    	id1=Configurations[conf]

    elif States["actual"]== "0000001" or States["actual"]== "0000010" or States["actual"]== "0000011":
    	conf="Cam1Der"
    	id1=Configurations[conf]


    elif States["pasado"]=="0000000" and States["actual"]=="0000000":
    	if States["antepasado"]=="1000000":
    		conf="Cam1S1"
    		id1=Configurations[conf]
    	if States["antepasado"]=="0100000":
    		conf="Cam1S2"
    		id1=Configurations[conf]
    	if States["antepasado"]=="0010000":
    		conf="Cam1S3"
    		id1=Configurations[conf]
    	if States["antepasado"]=="0001000":
    		conf="Cam1S4"
    		id1=Configurations[conf]
    	if States["antepasado"]=="0000100":
    		conf="Cam1S5"
    		id1=Configurations[conf]
    	if States["antepasado"]=="0000010":
    		conf="Cam1S6"
    		id1=Configurations[conf]
    	if States["antepasado"]=="0000001":
    		conf="Cam1S7"
    		id1=Configurations[conf]

	id_preset=id1
    if id_inicial!=id_preset:
        telnet.write('xCommand Camera Preset Activate PresetId:'+str(id1)+'\n')
        telnet.read_until('OK')


	time.sleep(0.3)
	GPIO.output(23,0)
	time.sleep(0.2)

	cadena_inicial=str(S1)+str(S2)+str(S3)+str(S4)+str(S5)+str(S6)+str(S7)