import random
from tqdm.auto import tqdm

LEN = 13017753

progress_bar = tqdm(range(100000 + 500000 + 1000000 + 1000))

indexes = [i for i in range(LEN)]
random.shuffle(indexes)
indexes_100000 = indexes[:100000]
indexes_500000 = indexes[:500000]
indexes_1000000 = indexes[:1000000]
indexes_test = indexes[1000000:1001000]

indexes_100000.sort()
indexes_500000.sort()
indexes_1000000.sort()
indexes_test.sort()

file_read = open('D:/alignments_gpu', 'r')
file_1 = open('D:/alignments_100000', 'w')
file_2 = open('D:/alignments_500000', 'w')
file_3 = open('D:/alignments_1000000', 'w')
file_4 = open('D:/alignments_test', 'w')

current1 = 0
current2 = 0
current3 = 0
current4 = 0

for pos, line in enumerate(file_read):
    if current1 < 100000 and pos == indexes_100000[current1]:
        file_1.write(line)
        progress_bar.update(1)
        current1 += 1
    if current2 < 500000 and pos == indexes_500000[current2]:
        file_2.write(line)
        progress_bar.update(1)
        current2 += 1
    if current3 < 1000000 and pos == indexes_1000000[current3]:
        file_3.write(line)
        progress_bar.update(1)
        current3 += 1
    if current4 < 1000 and pos == indexes_test[current4]:
        file_4.write(line)
        progress_bar.update(1)
        current4 += 1   

file_read.close()
file_1.close()
file_2.close()
file_3.close()
file_4.close()