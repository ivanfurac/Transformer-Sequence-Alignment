from Bio.Align import PairwiseAligner, substitution_matrices

def get_aligner(open_gap_score):
    aligner = PairwiseAligner()
    aligner.mode = 'global'
    aligner.open_gap_score = open_gap_score
    aligner.extend_gap_score = -1
    aligner.substitution_matrix = substitution_matrices.load('BLOSUM62')
    return aligner    

def generate_inputs(pair):
    seq1 = " ".join(pair[0])
    seq2 = " ".join(pair[1])
    return seq1 + " | " + seq2

def generate_outputs(pair):
    seq1 = pair[0]
    seq2 = pair[1]
    output = ""
    for index in range(len(seq1)):
        element1 = 'x' if seq1[index] == '-' else seq1[index]
        element2 = 'x' if seq2[index] == '-' else seq2[index]
        output = output + element1 + element2 + ' '
    return output[:-1]

path_read =  'pairs/gap0/alignments_test'
path_gap3 = 'pairs/gap3/alignments_test'
path_gap5 = 'pairs/gap5/alignments_test'
path_gap11 = 'pairs/gap11/alignments_test'

file_read = open(path_read, 'r')
file_gap3 = open(path_gap3, 'w')
file_gap5 = open(path_gap5, 'w')
file_gap11 = open(path_gap11, 'w')

length = 0
diff = 0

aligner_gap3 = get_aligner(-3)
aligner_gap5 = get_aligner(-5)
aligner_gap11 = get_aligner(-11)

for pos, line in enumerate(file_read):
    line_split = line.strip('\n').split('\t')
    seq1 = line_split[0].split('|')[0].strip().replace(' ', '')
    seq2 = line_split[0].split('|')[1].strip().replace(' ', '')
    length += len(seq1)
    length += len(seq2)
    diff += abs(len(seq1) - len(seq2))
    
    alignment_gap3 = aligner_gap3.align(seq1, seq2)
    optimal = next(alignment_gap3)
    a_str = optimal.format()            
    al1 = a_str.split('\n')[0]
    al2 = a_str.split('\n')[2]
    file_gap3.write(generate_inputs((seq1, seq2)) + "\t" + generate_outputs((al1, al2)) + "\t" + str(optimal.score) + "\n")
    
    alignment_gap5 = aligner_gap5.align(seq1, seq2)
    optimal = next(alignment_gap5)
    a_str = optimal.format()            
    al1 = a_str.split('\n')[0]
    al2 = a_str.split('\n')[2]
    file_gap5.write(generate_inputs((seq1, seq2)) + "\t" + generate_outputs((al1, al2)) + "\t" + str(optimal.score) + "\n")
    
    alignment_gap11 = aligner_gap11.align(seq1, seq2)
    optimal = next(alignment_gap11)
    a_str = optimal.format()            
    al1 = a_str.split('\n')[0]
    al2 = a_str.split('\n')[2]
    file_gap11.write(generate_inputs((seq1, seq2)) + "\t" + generate_outputs((al1, al2)) + "\t" + str(optimal.score) + "\n")

print('PROSJECNA DULJINA SLJEDOVA:')
print(float(length/1000000))

print('PROSJECNA RAZLIKA:')
print(float(diff/1000000))

file_read.close()
file_gap3.close()
file_gap5.close()
file_gap11.close()