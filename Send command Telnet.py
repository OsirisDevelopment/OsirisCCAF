from telnetlib import Telnet
import time
telnet = Telnet('192.168.29.111', 23)
telnet.read_until('login:')
telnet.write('admin\n')
telnet.read_until('Password:')
telnet.write('\n')
telnet.read_until('OK')

print telnet.write('xCommand Standby Deactivate\n')
print telnet.read_until('OK')
time.sleep(1)
print telnet.write('xCommand Camera Preset Activate PresetId:1\n')
print telnet.read_until('OK')
