import time
import json
import platform
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


def add_new_entry(value_one, value_two, value_three, value_four):
    packet_frequency.append(value_one)
    processor_time.append(value_two)
    io_operations.append(value_three)
    memory_usage.append(value_four)


def write_values():
    data = {}
    data['packet_frequency'] = average(packet_frequency)
    data['processor_time'] = average(processor_time)
    data['io_operations'] = average(io_operations)
    data['memory_usage'] = average(memory_usage)
    print(data)
    write_to_file(data)


def write_to_file(dict_data):
    f = open("data.json", 'w')
    f.write(json.dumps(dict_data))
    f.close()


def tail(filename, n = 50):
    return deque(open(filename, 'r'), n)


def main():
    while(1):
        if platform.system() == 'Windows':
            log = tail("C:\PerfLogs\\notepad_log.csv", MAX_ENTRIES)
        else:
            log = tail("notepad_log.csv", MAX_ENTRIES)
        for entry in log:
            values = entry.split('"')
            if bool(values[3].strip()):
                add_new_entry(float(values[3]), float(values[5]), float(values[7]), float(values[9]))
            else:
                add_new_entry(0, 0, 0, 0)

            write_values()
            time.sleep(1)

            if len(memory_usage) >= MAX_ENTRIES:
                remove_last_entry()


main()
