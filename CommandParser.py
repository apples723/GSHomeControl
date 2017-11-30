from phue import Bridge
import requests
import urllib

request = urllib.request.Request('http://randomster.co/sh/c.txt')  
result = urllib.request.urlopen(request)          
lines = []
for line in result:
	lines.append(line.rstrip())

#prepare connection to bridge
b = Bridge('192.168.1.3')
	
if lines[1] == b'On':
	print(1)
	litnum = int(lines[0].decode('utf-8'))
	b.set_light(litnum, 'on', True)
if lines[1] == 'Off':
	print(2)
	litnum = int(lines[0].decode('utf-8'))
	b.set_light(litnum, 'on', False)
if lines[1] == b'bri':
	print(3)
	litnum = int(lines[0].decode('utf-8'))
	brinum = int(lines[2].decode('utf-8'))
	b.set_light(litnum, 'bri', brinum)


	

	