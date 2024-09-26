'''
Кол-во интерфейсов 1.3.6.1.2.1.2.1.0

Название интерфейса 1.3.6.1.2.1.2.2.1.2.{k} 

STATE 1.3.6.1.2.1.2.2.1.8.{k} (1-up, 2-down, 3-testing, 4-unknown, 5-dormant, 6-notPresent, 7-lowerLayerDown):

IN OCTET1.3.6.1.2.1.2.2.1.10.{k} (bytes)

OUT OCTET 1.3.6.1.2.1.2.2.1.16.{k} (bytes)
'''

from easysnmp import snmp_get, snmp_set, snmp_walk
# Perform an SNMP walk
print(snmp_walk('1.3.6.1.2.1.2.2.1.2', hostname='10.116.35.1', community='cisco', version=1))