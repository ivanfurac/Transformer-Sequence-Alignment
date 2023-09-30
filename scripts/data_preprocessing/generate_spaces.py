folders = ['/gap5/']
files = ['alignments_200_gap5_100000', 'alignments_200_gap5_test']

for folder in folders:
    for file in files:
        path = folder + file
        f_read = open('pairs' + path, 'r')
        f_write = open('spaces' + path, 'w')
        
        for pos, line in enumerate(f_read):
            line_split = line.strip('\n').split('\t')
            unaligned = line_split[0]
            aligned = line_split[1].replace(' ', '')
            score = line_split[2]
            aligned_new = " ".join(aligned)
            f_write.write(unaligned + "\t" + aligned_new + "\t" + score + "\n")
        
        f_write.close()
        f_read.close()