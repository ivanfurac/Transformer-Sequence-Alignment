from BLOSUM62 import BLOSUM62

def accuracy(output, target):
    len_output = len(output)
    len_target = len(target)
    
    score = 0
    for i in range(min(len_target, len_output)):
        if(output[i] == target[i]):
            score += 1
            
    return score / len_target

def coverage(output, target1, target2, gap_character = 'x'):
    output1 = ''
    output2 = ''
    for pair in output:
        if(pair[0] != gap_character):
            output1 += pair[0]
        if(pair[1] != gap_character):
            output2 += pair[1]
    
    
    coverage1 = 0
    coverage2 = 0
    
    for i in range(min(len(output1), len(target1))):
        if(output1[i] == target1[i]):
            coverage1 += 1
        
    for i in range(min(len(output2), len(target2))):
        if(output2[i] == target2[i]):
            coverage2 += 1
            
    return (coverage1/len(target1), coverage2/len(target2))

def alignment_score(output, gap_open_penalty = -5, gap_extend_penalty = -1, substitution_matrix = BLOSUM62, gap_character = 'x'):
    
    score = 0
    
    gap_extend = False
    
    for pair in output:
        if gap_character in pair and gap_extend is False:
            gap_extend = True
            score += gap_open_penalty
        elif gap_character in pair and gap_extend is True:
            score += gap_extend_penalty
        else:
            score += substitution_matrix[pair[0], pair[1]]
            gap_extend = False
            
    return score 
