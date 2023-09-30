from Bio.Align import substitution_matrices

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

blosum62 = substitution_matrices.load('BLOSUM62')

dict_elements = []

for a1 in aminoacids:
    for a2 in aminoacids:
        value = blosum62[a1, a2]
        dict_elements.append('(\'' + a1 + '\', \'' + a2 + '\'): ' + str(value))
        
print(dict_elements)

code = 'BLOSUM62 = {'
for el in dict_elements:
    code = code + el + ', '

print(code)