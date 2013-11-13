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


def average(seq):
    sum = 0
    for x in seq:
        sum = sum + x
    return sum / len(seq) if len(seq) > 0 else 0


def remove_last_entry():
    packet_frequency.popleft()
    processor_time.popleft()
    io_operations.popleft()
    memory_usage.popleft()


def add_new_entry(values):
    if bool(values[3].strip() and values[5].strip()):
        packet_frequency.append(float(values[3]))
        processor_time.append(float(values[5]))
        io_operations.append(float(values[7]))
        memory_usage.append(float(values[9]))
    else:
        add_new_entry(0, 0, 0, 0)


def store_values_to_hash():
    data = {}
    data['packet_frequency'] = average(packet_frequency)
    data['processor_time'] = average(processor_time)
    data['io_operations'] = average(io_operations)
    data['memory_usage'] = average(memory_usage)
    return data

def write_to_file(dict_data):
    print(dict_data)
    f = open("data.json", 'w')
    f.write(json.dumps(dict_data))
    f.close()


def tail(filename, n = 50):
    return deque(open(filename, 'r'), n)


def read_log_from_file():
    if platform.system() == 'Windows':
        return tail("C:\PerfLogs\\notepad_log.csv", MAX_ENTRIES)
    else:
        return tail("notepad_log.csv", MAX_ENTRIES)


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
    return ['ntdll.dll', 'kernel32.dll', 'comdlg32.dll', 'ADVAPI32.dll', 'RPCRT4.dll', 'Secur32.dll', 'COMCTL32.dll', 'msvcrt.dll', 'GDI32.dll', 'USER32.dll', 'SHLWAPI.dll', 'SHELL32.dll', 'WINSPOOL.DRV', 'ShimEng.dll', 'AcGenral.DLL', 'WINMM.dll', 'ole32.dll', 'OLEAUT32.dll', 'MSACM32.dll', 'VERSION.dll', 'USERENV.dll', 'UxTheme.dll']


def main():
    while(1):
        log = read_log_from_file()
        for entry in log:
            add_new_entry(entry.split('"'))
            if len(memory_usage) >= MAX_ENTRIES: remove_last_entry()
            data = store_values_to_hash()

            if platform.system() == 'Windows': list_dlls()
            data['dll_list'] = dll_parser()
            write_to_file(data)
            time.sleep(1)


main()
