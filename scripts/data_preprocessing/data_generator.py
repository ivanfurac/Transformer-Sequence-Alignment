from Bio import SeqIO
from random import shuffle

def generate_inputs(pair):
    seq1 = " ".join(pair[0].replace("-", ""))
    seq2 = " ".join(pair[1].replace("-", ""))
    return seq1 + " | " + seq2

def generate_outputs(pair):
    seq1 = pair[0]
    seq2 = pair[1]
    output = ""
    for index in range(len(seq1)):
        if(seq1[index] == '-' and seq2[index] == '-'):
            continue
        element1 = 'x' if seq1[index] == '-' else seq1[index]
        element2 = 'x' if seq2[index] == '-' else seq2[index]
        output = output + element1 + element2 + ' '
    return output[:-1]

data_path = './fasta/vpr.fasta'
output_path = './data/alignments'

sequences = []

for seq in SeqIO.parse(data_path, 'fasta'):
    if('#' in seq or 'X' in seq):
        continue
    sequences.append(seq.seq[:-1])
    
shuffle(sequences) 
selected_sequences = sequences

pairs = [(a, b) for idx, a in enumerate(selected_sequences) for b in selected_sequences[idx + 1:]]

with open(output_path, "w") as f:
    for pair in pairs:
        f.write(generate_inputs(pair) + "\t" + generate_outputs(pair) + "\n")