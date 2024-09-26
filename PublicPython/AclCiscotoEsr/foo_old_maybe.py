import netmiko
f = open('2.txt', 'r')
a = {
	'0.0.0.0': '/0',
	'255.0.0.0': '/8',
	'255.255.255.224': '/27',
	'255.255.255.192': '/26',
	'255.255.128.0': '/17',
	'255.255.255.0':'/24',
	'255.255.0.0': '/16',
	'255.255.255.252': '/30',
	'255.255.255.255': '/32'
}
c = {
	'device_type': 'eltex',
	'host': '1.1.1.1',
	'username': 'admin',
	'password': 'admin',
	'secret': 'admin',
	'port': 22,
}
al = []
co = 1
name_ac = 'to_vipnet_154'
ssh = netmiko.ConnectHandler(**c)
for i in f.read().split('\n'):
	print(i.split(' '))	
	if i.split(' ')[1] == 'permit':
		act = 'action permit'
		if i.split(' ')[3] == 'host':
			so_ad_msk = '255.255.255.255'
			so_ad = i.split(' ')[4]
			if i.split(' ')[5] == 'any':
				d_ad_a_msk = 'any'
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad} {so_ad_msk}', f'ma destination-a {d_ad_a_msk}', 'ma pro an', 'enable'] 
			elif i.split(' ')[5] == 'host':
				d_msk = '255.255.255.255'
				d_ad = i.split(' ')[6]
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad} {so_ad_msk}', f'ma destination-a {d_ad} {d_msk}', 'ma pro an', 'enable'] 
			else:
				d_ad = i.split(' ')[5]
				d_msk = []
				for bits in i.split(' ')[6].split('.'):
					d_msk.append(str(255 - int(bits)))
				d_msk = '.'.join(d_msk)
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad} {so_ad_msk}', f'ma destination-a {d_ad} {d_msk}', 'ma pro an', 'enable'] 
		elif i.split(' ')[3] == 'any':
			so_ad_a_msk = 'any'
			if i.split(' ')[4] == 'host':
				d_msk = '255.255.255.255'
				d_ad = i.split(' ')[5]
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad_a_msk}', f'ma destination-a {d_ad} {d_msk}', 'ma pro an', 'enable'] 
			elif i.split(' ')[4] == 'any':
				d_ad_a_msk = 'any'
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad_a_msk}', f'ma destiantion-a {d_ad_a_msk}', 'ma pro an', 'enable'] 
			else:
				d_ad = i.split(' ')[4]
				d_msk = []
				for bits in i.split(' ')[5].split('.'):
					d_msk.append(str(255 - int(bits)))
				d_msk = '.'.join(d_msk)
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad_a_msk}', f'ma destination-a {d_ad} {d_msk}', 'ma pro an', 'enable'] 
		else:
			so_ad = i.split(' ')[3]
			so_ad_msk = i.split(' ')[4]
			if i.split(' ')[5] == 'host':
				d_msk = '255.255.255.255'
				d_ad = i.split(' ')[6]
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad} {so_ad_msk}', f'ma destination-a {d_ad} {d_msk}', 'ma pro an', 'enable'] 
			elif i.split(' ')[5] == 'any':
				d_ad_a_msk = 'any'
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad} {so_ad_msk}', f'ma destination-a {d_ad_a_msk}', 'ma pro an', 'enable'] 
			else:
				d_msk = []
				for bits in i.split(' ')[6].split('.'):
					d_msk.append(str(255 - int(bits)))
				d_msk = '.'.join(d_msk)
				d_ad = i.split(' ')[5]
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad} {so_ad_msk}', f'ma destination-a {d_ad} {d_msk}', 'ma pro an', 'enable'] 
	elif i.split(' ')[1] == 'deny':
		act = 'action deny'
		if i.split(' ')[5] == 'host':
			so_ad = i.split(' ')[6]
			so_ad_msk = '255.255.255.255'
			if i.split(' ')[7] == 'host':
				d_ad = i.split(' ')[8]
				d_msk = '255.255.255.255'
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad} {so_ad_msk}', f'ma destination-a {d_ad} {d_msk}', 'ma pro an', 'enable']
			elif i.split(' ')[7] == 'any':
				d_ad_a_msk = 'any'
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad} {so_ad_msk}', f'ma destination-a {d_ad_a_msk}', 'ma pro an', 'enable']
			else:
				d_ad = i.split(' ')[7]
				d_msk = []
				for bits in i.split(' ')[8].split('.'):
					d_msk.append(str(255 - int(bits)))
				d_msk = '.'.join(d_msk)
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad} {so_ad_msk}', f'ma destination-a {d_ad} {d_msk}', 'ma pro an', 'enable']
		elif i.split(' ')[5] == 'any':
			so_ad_a_msk = 'any'
			if i.split(' ')[6] == 'host':
				d_ad = i.split(' ')[7]
				d_msk = '255.255.255.255'
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad_a_msk}', f'ma destination-a {d_ad} {d_msk}', 'ma pro an', 'enable']
			elif i.split(' ')[6] == 'any':
				d_ad_a_msk = 'any'
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad_a_msk}', f'ma destination-a {d_ad_a_msk}', 'ma pro an', 'enable']
			else:
				d_ad = i.split(' ')[6]
				d_msk = []
				for bits in i.split(' ')[7].split('.'):
					d_msk.append(str(255 - int(bits)))
				d_msk = '.'.join(d_msk)
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad_a_msk}', f'ma destination-a {d_ad} {d_msk}', 'ma pro an', 'enable']
		else:
			so_ad = i.split(' ')[5]
			so_ad_msk = i.split(' ')[6]
			if i.split(' ')[7] == 'host':
				d_ad = i.split(' ')[8]
				d_msk = '255.255.255.255'
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad} {so_ad_msk}', f'ma destination-a {d_ad} {d_msk}', 'ma pro an', 'enable']
			elif i.split(' ')[7] == 'any':
				d_ad_a_msk = 'any'
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad} {so_ad_msk}', f'ma destination-a {d_ad_a_msk}', 'ma pro an', 'enable']
			else:
				d_ad = i.split(' ')[7]
				d_msk = []
				for bits in i.split(' ')[8].split('.'):
					d_msk.append(str(255 - int(bits)))
				d_msk = '.'.join(d_msk)
				al = [f'ip ac ex {name_ac}', f'rule {co}', act, f'ma source-a {so_ad} {so_ad_msk}', f'ma destination-a {d_ad} {d_msk}', 'ma pro an', 'enable']
	#print(*al)
	#al.append(i.split(' ')[3])
	print(al,'\n\n\n')
	print(ssh.send_config_set(al))
	co += 1
ssh.disconnect()
f.close()

#print(set(al))