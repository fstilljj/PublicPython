with open('ZABA.txt', 'r', encoding = 'utf-8') as file:
	for i in file.read().split('\n'):
		host_name = i.split(':')[1]
		visible_name = i.split(':')[0]
		ip_address = i.split(':')[1]
		snmp_community = 'cisco'  # SNMP community
		snmp_version = 2  # SNMP version (2 for SNMPv2)
		snmp_port = 161  # SNMP port
		gr = "10218" if i.split(':')[3] == 'cisco' else '10610'
		zapi.host.create(
		    host=host_name, #IP 
		    name=visible_name,
		    interfaces=[{
		        "type": 2,
		        "main": 1,
		        "useip": 1,
		        "ip": ip_address,
		        "dns": "",
		        "port": "161",
		        "details": {
		            "version": snmp_version,
		            "community": snmp_community,
		        }
		    }],
		    groups=[{
		        "groupid": '2'
		    }],
		    templates=[{
		        "templateid": gr
		    }]
		)