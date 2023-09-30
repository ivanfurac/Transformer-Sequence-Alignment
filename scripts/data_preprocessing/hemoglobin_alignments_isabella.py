from Bio import SeqIO
from Bio.Align import PairwiseAligner, substitution_matrices

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

data_path = 'hemoglobin.fasta'
output_path5 = 'alignments_100_gap5'
output_path11 = 'alignments_100_gap11'

sequences = []

for seq in SeqIO.parse(data_path, 'fasta'):
    if(len(seq) <= 100 and len(sequences < 3500)):
        sequences.append(seq.seq)

file5 = open(output_path5, 'w')
file11 = open(output_path11, 'w')

aligner5 = PairwiseAligner()
aligner5.mode = 'global'
aligner5.open_gap_score = -5
aligner5.extend_gap_score = -1
aligner5.substitution_matrix = substitution_matrices.load('BLOSUM62')

aligner11 = PairwiseAligner()
aligner11.mode = 'global'
aligner11.open_gap_score = -11
aligner11.extend_gap_score = -1
aligner11.substitution_matrix = substitution_matrices.load('BLOSUM62')

avg_length = 0
max_length = 0
min_length = 100
diff = 0

for i in range(len(sequences)):
    for j in range(i+1, len(sequences)):
        seq1 = sequences[i]
        seq2 = sequences[j]
        
        try:
            alignment_gap5 = aligner5.align(seq1, seq2)
            alignment_gap11 = aligner11.align(seq1, seq2)
        except:
            print('Error')
        else:            
            optimal = next(alignment_gap5)
            a_str = optimal.format()            
            al1 = a_str.split('\n')[0]
            al2 = a_str.split('\n')[2]
            file5.write(generate_inputs((seq1, seq2)) + "\t" + generate_outputs((al1, al2)) + "\t" + str(optimal.score) + "\n")
    
            optimal = next(alignment_gap11)
            a_str = optimal.format()            
            al1 = a_str.split('\n')[0]
            al2 = a_str.split('\n')[2]
            file11.write(generate_inputs((seq1, seq2)) + "\t" + generate_outputs((al1, al2)) + "\t" + str(optimal.score) + "\n")
            
            avg_length = avg_length + len(seq1) + len(seq2)
            if(len(seq1) > max_length):
                max_length = len(seq1)            
            if(len(seq1) < min_length):
                min_length = len(seq1)            
            diff += abs(len(seq1) - len(seq2))
            
print(float(avg_length / len(avg_length)))
print(max_length)
print(min_length)
print(float(diff / len(diff)))