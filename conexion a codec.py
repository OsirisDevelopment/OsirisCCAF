from telnetlib import Telnet

#conexion

#puertos
#22 SSH
#23 Telnet

#                  IP del codec , Telnet
telnet = Telnet('192.168.29.111', 23)
telnet.read_until('login:')
telnet.write('admin\n')
telnet.read_until('Password:')
telnet.write('\n')
telnet.read_until('OK')

#wake up camara si esta en modo StandBy
telnet.write('xCommand Standby Deactivate\n')
telnet.read_until('OK')


#Envio de comando para el posicionamiento de la camara
telnet.write('xCommand Camera Preset Activate PresetId:'+str(id1)+'\n')
telnet.read_until('OK')
