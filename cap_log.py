import csv

def read_file():
    with open('device_list.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        list_of_rows = list(csv_reader)
        return list_of_rows

def device_login(device_info):
    host_ip = device_info[0]
    username = device_info[1]
    password = device_info[2]
    device_type = device_info[3]

    if len(device_info) == 5 and device_type == 'ios':
        enable_password =  device_info[4]
    else:
        enable_password = "]"



def device_cmd_execute():
    pass

def save_output_to_file():
    pass

def main():
    device_info_list = read_file()
    for device_info in device_info_list:
        device_login(device_info)

if __name__ == '__main__':
    main()
