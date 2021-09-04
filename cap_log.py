import csv
import paramiko
import time
from datetime import datetime

from paramiko.ssh_exception import AuthenticationException, BadAuthenticationType, BadHostKeyException, ChannelException, NoValidConnectionsError, PasswordRequiredException, SSHException

def read_file(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        list_of_rows = list(csv_reader)
        return list_of_rows

def capture_log(device_info):
    host_ip = device_info[0]
    username = device_info[1]
    password = device_info[2]
    device_outputs = ''


    print('Working on ' + host_ip)
    print('...')

        
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host_ip, port=22, username=username, password=password)

    connection = ssh.invoke_shell()
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
    ssh.close()

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
    failed_device_log = ''
    for device_info in device_info_list:
        try:
            capture_log(device_info)
            print('Done')
            print('=' * 15)
        except (AuthenticationException, BadAuthenticationType, ChannelException, NoValidConnectionsError, PasswordRequiredException, EOFError) as e:
            failed_device_log = failed_device_log + str(device_info[0]) + ' ' + str(e) + '\n'           
            pass
    save_file('failed_log.txt', failed_device_log)

if __name__ == '__main__':
    main()