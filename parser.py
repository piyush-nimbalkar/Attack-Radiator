import re
import time
import json
import platform
from subprocess import call
from collections import deque


MAX_ENTRIES = 10
packet_frequency = deque([])
processor_time = deque([])
io_operations = deque([])
memory_usage = deque([])


def read_log_from_file():
    if platform.system() == 'Windows':
        return tail("C:\PerfLogs\\notepad_log.csv")
    else:
        return tail("notepad_log.csv")


def tail(filename, n = 1):
    return deque(open(filename, 'r'), n)


def add_new_entry(value_1, value_2, value_3, value_4):
    packet_frequency.append(value_1)
    processor_time.append(value_2)
    io_operations.append(value_3)
    memory_usage.append(value_4)


def remove_last_entry():
    packet_frequency.popleft()
    processor_time.popleft()
    io_operations.popleft()
    memory_usage.popleft()


def store_values_to_hash():
    data = {}
    data['packet_frequency'] = average(packet_frequency)
    data['processor_time'] = average(processor_time)
    data['io_operations'] = average(io_operations)
    data['memory_usage'] = average(memory_usage)
    return data


def average(seq):
    sum = 0
    for x in seq:
        sum = sum + x
    return sum / len(seq) if len(seq) > 0 else 0


def list_dlls():
    f = open('dll_list.txt', 'w')
    text = call(['Listdlls.exe', 'notepad.exe'], stdout = f)
    f.close()


def dll_parser():
    file = open("dll_list.txt", 'r')
    malicious_list = []
    for line in file:
        result = re.search('(\w+\.dll)', line)
        if result and not (result.group(1) in original_list()):
            malicious_list.append(result.group(1))
    file.close()
    return malicious_list


def original_list():
    file = open('original_dll_list.txt', 'r')
    dlls = []
    for line in file:
        dlls.append(line.strip())
    file.close()
    return dlls


def write_to_file(dict_data):
    print(dict_data)
    f = open("data.json", 'w')
    f.write(json.dumps(dict_data))
    f.close()


def main():
    while(1):
        log = read_log_from_file()
        for entry in log:
            values = entry.split('"')
            if bool(values[3].strip() and values[5].strip()):
                add_new_entry(float(values[3]), float(values[5]), float(values[7]), float(values[9]))
            else:
                add_new_entry(0, 0, 0, 0)

            if len(memory_usage) >= MAX_ENTRIES: remove_last_entry()
            data = store_values_to_hash()

            if platform.system() == 'Windows': list_dlls()
            data['dll_list'] = dll_parser()
            write_to_file(data)
            time.sleep(2)


main()
