def connect(ip, username, passwd, driver):
        tftp = '1.1.1.1'
        data_router = {
        'device_type': driver,
        'host': ip,
        'username': username,
        'password': passwd,
        'secret': passwd,
        'port': 22,
        }
        try:
                with netmiko.ConnectHandler(**data_router) as ssh:
                        if driver == 'eltex':
                                out = ssh.send_command(f'copy run tftp://{tftp}/{ip}_{date.today()}.txt')
                                if 'syntax' in out.lower():
                                        out = ssh.send_command(f'copy fs://running-config tftp://{tftp}:/{ip}_{date.today()}.txt')
                                        if 'syntax' in out.lower():
                                                out = ssh.send_command(f'copy system:running-config tftp://{tftp}:/{ip}_{date.today()}.txt')
                        else:
                                print(ssh.send_command(f'copy run tftp://{tftp}/{ip}_{date.today()}.txt', expect_string = ']?'))
                                print(ssh.send_command('\n', expect_string = ']?'))

        except netmiko.exceptions.NetMikoTimeoutException:
                try:
                        data_router['port'] = 23
                        data_router['device_type'] = 'cisco_ios_telnet'
                        print(data_router)
                        with netmiko.ConnectHandler(**data_router) as ssh:
                                print(ssh.send_command(f'copy run tftp://{tftp}/{ip}_{date.today()}.txt', expect_string = ']?'))
                                print(ssh.send_command('\n', expect_string = ']?'))
                except Exception as Ex:
                        print(Ex)
        except Exception as Ex:
                print(Ex)

def ssh():
        a = f'ls /home/guit/Documents/tftp | grep {date.today()}'
        b = subprocess.run(a, stdout=subprocess.PIPE, shell=True)
        c = b.stdout.decode('utf-8')
        spis = []
        for i in c.split('\n'):
                spis.append(i)
        with open('/home/guit/Documents/python_scripts/tftp_script/a.txt', 'r', encoding='utf-8') as file:
                for i in file.read().split('\n'):
                        if i != '':
                                if i.split(':')[1] not in spis:
                                        os.system(f'''echo "{i.split(':')[1]}" >> "NOT_{date.today()}"''')

def main():
        with open('a.txt', 'r', encoding = 'utf-8') as file:
                for stroka in file.read().split('\n'):
                        if stroka != '':
                                print(stroka)
                                ip = stroka.split(':')[1]
                                if ping(ip):
                                        username = stroka.split(':')[2].split('/')[0]
                                        passwd = stroka.split(':')[2].split('/')[1]
                                        if stroka.split(':')[3] == 'eltex':
                                                connect(ip, username, passwd, 'eltex')
                                        else:
                                                connect(ip, username, passwd, 'cisco_ios')
                ssh()

if __name__ == '__main__':
        import netmiko, schedule, time, os, subprocess
        from datetime import date
        from ping3 import ping, verbose_ping
        cont = ''
        schedule.every().day.at("18:00").do(main)
        while True:
                schedule.run_pending()
                time.sleep(1)