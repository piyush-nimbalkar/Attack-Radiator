import time
import json
from collections import deque


MAX_ENTRIES = 10
memory_usage = deque([])
processor_time = deque([])
io_operations = deque([])


def average(seq):
    sum = 0
    for x in seq:
        sum = sum + x
    return sum / len(seq)


def remove_last_entry():
    processor_time.popleft()
    io_operations.popleft()
    memory_usage.popleft()


def add_new_entry(value_one, value_two, value_three):
    processor_time.append(value_one)
    io_operations.append(value_two)
    memory_usage.append(value_three)


def write_values():
    data = {}
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
        # log = tail("C:\PerfLogs\\Notepad.csv", MAX_ENTRIES) # for Windows
        log = tail("data.csv", MAX_ENTRIES) # for development in Linux
        for entry in log:
            values = entry.split('"')
            add_new_entry(float(values[3]), float(values[5]), float(values[7]))

            write_values()
            time.sleep(0.5)

            if len(memory_usage) >= MAX_ENTRIES:
                remove_last_entry()


main()
