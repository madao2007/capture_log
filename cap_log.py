import csv
import paramiko
import time
from datetime import datetime

def read_file(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        list_of_rows = list(csv_reader)
        return list_of_rows


def capture_log(device_info):
    host_ip = device_info[0]
    username = device_info[1]
    password = device_info[2]
    device_type = device_info[3]
    device_outputs = ''
    enable_password = ''

    print('Working on ' + host_ip)
    print('...')

    if len(device_info) == 5 and device_type == 'ios':
        enable_password =  device_info[4]
        
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=host_ip, port=22, username=username, password=password)
    connection = ssh.invoke_shell()
    if device_type == 'ios':
        prompt_out = str(connection.recv(9999))
        prompt_out = prompt_out.split('\n')[-1]
        if '#' not in prompt_out:
            connection.send("enable")
            connection.send('\n')
            time.sleep(1)
            connection.send(enable_password) 
            connection.send('\n')

    command_list = read_file('command_list.csv')
    count = 0
    for command in command_list:
        connection.send(command[0])
        connection.send('\n')
        print(command[0])
        time.sleep(1)
        file_output = connection.recv(9999999).decode(encoding='utf-8')
        device_outputs += file_output

        if count == 0:
            host_name = file_output.split('\n')[-1].split('#')[0]
        count += 1

    curret_date = datetime.today().strftime('%Y-%m-%d-%H-%M')
    file_name = curret_date + '_' + host_name

    save_file(file_name, device_outputs)

def save_file(file_name, content):
    file = './show-output/' + file_name + '.txt'
    f = open(str(file), 'a+')
    f.write(content)
    f.close()
        

def main():
    device_info_list = read_file('device_list.csv')
    for device_info in device_info_list:
        capture_log(device_info)
        print('Done')
        print('=' * 15)

if __name__ == '__main__':
    main()
