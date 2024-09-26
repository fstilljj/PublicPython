
def main():
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
	with open('2.txt', 'r') as file:
		for i in file.read().split('\n'):
			ste = i.split(' ')
			with netmiko.ConnectHandler(**c) as ssh:
				print(ssh.send_config_set([f'ip route {ste[2]}{a[ste[3]]} {ste[4]}']))


if __name__ == '__main__':
	import netmiko
	main()