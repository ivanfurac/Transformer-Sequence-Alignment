aminoacids = [
    'A',
    'R',
    'N',
    'D',
    'C',
    'H',
    'F',
    'G',
    'Q',
    'E',
    'I',
    'L',
    'K',
    'M',
    'P',
    'S',
    'Y',
    'T',
    'W',
    'V'    
]

input_dict = './data/input_dict'
output_dict = './data/output_dict'

with open(input_dict, 'w') as f:
    f.write('?\n')
    f.write('[MASK]\n')
    f.write('|\n')
    for aa in aminoacids:
        f.write(aa + '\n')
        
with open(output_dict, 'w') as f:
    f.write('?\n')
    f.write('[MASK]\n')
    f.write('START\n')
    f.write('END\n')
    for aa in aminoacids:
        f.write(aa + 'x\n')
        f.write('x' + aa + '\n')
        for aa2 in aminoacids:
            f.write(aa + aa2 + '\n')