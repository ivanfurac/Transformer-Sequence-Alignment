import numpy as np

#file = open('l3h8d128', 'r')
file = open('spaces_l3h8d128_results', 'r')
lines = file.readlines()
file.close()

cs_avg = 0
cov_avg = 0
score_real_avg = 0
score_my_avg = 0

scores_abs = []
scores_rel = []

num = 0

for line in lines:
    if('0' in line):
        cs = float(line.strip('\n').split('\t')[0])        
        if(cs >= 0.38):
            cs_avg += cs
        
            cov1 = float(line.strip('\n').split('\t')[1])
            cov2 = float(line.strip('\n').split('\t')[2])
            if(cov1 == 1.0):
                cov_avg += 1
            if(cov2 == 1.0):
                cov_avg += 1
        
            score_real = float(line.strip('\n').split('\t')[3])
            score_my = float(line.strip('\n').split('\t')[4]) 
                
            score_real_avg += score_real
            score_my_avg +=   score_my 
            
            scores_abs.append(abs(score_real - score_my))
            scores_rel.append(abs(score_real - score_my) / max(score_real, score_my))
            
            num += 1

print(num)
print(cov_avg / (2*num))
print(score_real_avg / num)
print(score_my_avg / num)
print(cs_avg / num)

print('\n')

print(np.mean(scores_abs))
print(np.std(scores_abs))

print(np.mean(scores_rel))
print(np.std(scores_rel))