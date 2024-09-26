from pyzabbix import ZabbixAPI
zapi = ZabbixAPI("http://zabbix.ru")
zapi.login("Admin", "zabbix")
templates = zapi.template.get(output="extend")

import openpyxl

# Load the workbook
workbook = openpyxl.load_workbook('IPIKA.xlsx')

# Select the active worksheet
worksheet = workbook.active
c = 0
# Access the cells
for row in worksheet.iter_rows(values_only=True):

	if c != 0:
		zapi.host.create(
			host=row[6],
			name=f'{row[1]} {row[2]} {row[4]}',
			interfaces=[{
				"type": 1,
				"main": 1,
				"useip": 1,
				"ip": row[6],
				"dns": "",
				"port": "161",
		}],
		groups=[{
			"groupid": '34'
		}],
		templates=[{
			"templateid": 10809
		}]
		)
	c +=1

