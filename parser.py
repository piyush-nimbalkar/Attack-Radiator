import time
import json
from collections import deque

def average(seq):
    sum = 0
    for x in seq:
        sum = sum + x
    return sum / len(seq)


def main():
    memory = deque([])
    processor_time = deque([])
    processor_io = deque([])
    max_entries = 10


    while(1):
        log = tail("C:\PerfLogs\\Notepad.csv", max_entries)
        # log = tail("data.csv", max_entries) # for development in ubuntu
        for entry in log:
            values = entry.split('"')
            memory.append(float(values[7]))
            processor_time.append(float(values[3]))
            processor_io.append(float(values[5]))

            dict_data = {}
            dict_data['processor_time'] = average(processor_time)
            dict_data['memory_usage'] = average(memory)
            dict_data['io_operations'] = average(processor_io)
            f = open("data.json", 'w')
            f.write(json.dumps(dict_data))
            f.close()

            print(average(processor_time), "  |  ", average(memory), "  |  ", average(processor_io))
            time.sleep(2)

            if len(memory) >= max_entries:
                memory.popleft()
                processor_time.popleft()
                processor_io.popleft()


def tail(filename, n = 50):
    return deque(open(filename, 'r'), n)


main()
