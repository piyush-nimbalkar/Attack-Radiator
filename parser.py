import csv
import time
from collections import deque

def average(seq):
    return reduce(lambda x, y: x+y, seq, 0) / len(seq)

def main1():
    memory = deque([])
    processor_time = deque([])
    processor_io = deque([])

    f = open('Calc_000001.csv', 'r')
    reader = csv.reader(f)
    reader.next()

    for r in reader:
        memory.append(float(r[6]))
        processor_time.append(float(r[1]))
        processor_io.append(float(r[2]))

        print average(memory), "  |  ", average(processor_time), "  |  ", average(processor_io)
        time.sleep(0.01)

        if len(memory) >= 10:
            memory.popleft()
            processor_time.popleft()
            processor_io.popleft()

    f.close()

main()
