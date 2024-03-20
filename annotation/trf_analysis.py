'''
Process the result file in dat format after running TFR

trf genome.fasta 2 7 7 80 10 50 500 -f -d -m -r -h

2023.3.12
'''
from collections import Counter

loci_start = []
loci_finish = []
total_line = []
with open('./genome.baima.fasta.2.7.7.80.10.50.500.dat', 'r') as input:
    for i in input.readlines()[15:]:
        if i.find('Sequence') != -1 or i.find('Parameters') != -1:
            continue
        else:
            lst = i.strip().split(' ')
            if len(lst) < 15:
                continue
            if len(loci_start) < 1 and len(loci_finish) < 1:   
                loci_start.append(lst[0])
                loci_finish.append(lst[1])
                total_line.append(lst)
            else:
                if lst[0] != loci_start[-1] and lst[1] != loci_finish[-1]:   
                    loci_start.append(lst[0])
                    loci_finish.append(lst[1])
                    total_line.append(lst)
                elif lst[0] == loci_start[-1]:        
                    continue
                elif lst[1] == loci_finish[-1]:       
                    del loci_start[-1]
                    del loci_finish[-1]
                    del total_line[-1]
                    loci_start.append(lst[0])
                    loci_finish.append(lst[1])
                    total_line.append(lst)

motif_lst = []
leng_lst = []
for i in total_line:
    motif_lst.append(i[2])
    leng = int(i[1]) - int(i[0]) + 1
    leng_lst.append(leng)

total_leng = {}
motif_sum = 0
for i in range(len(motif_lst)):
    item = motif_lst[i]
    motif_sum += leng_lst[i]
    if item in total_leng:
        total_leng[item] += leng_lst[i]
    else:
        total_leng[item] = leng_lst[i]

count_motif = Counter(motif_lst)
count_lst = list(count_motif.items())
count_lst.sort(key = lambda x : x[1], reverse = True)
lst_ = []
hit_num = 0
for i in count_lst:
    hit_num += i[1] 
for i in count_lst:
    ls = i[0]
    lst1 = list(i)
    if ls in total_leng:
        lst1.append(total_leng[ls])
    precentage = '%.2f%%'%(100 * i[1] / hit_num)
    lst1.append(precentage)
    lst_.append(lst1)

lst_filted = []
hit_ = 0
motif_ = 0
for i in range(1, 20):
    lst_filted.append(lst_[i])
    hit_ += lst_[i][1]
    motif_ += lst_[i][2]
lst_filted.append(['Other', int(hit_num - hit_), int(motif_sum - motif_), '%.2f%%'%(100 - 100 * hit_ / hit_num)])
lst_filted.append(['Total', int(hit_num), int(motif_sum), '100%'])


with open('./stastics.xls', 'w') as output:
    output.write('Motif(-mer)\tNumber\tLength(bp)\tPrecentage\n')
    for i in lst_filted:
        motif = i[0]
        number = i[1]
        length = i[2]
        pre = i[3]
        output.write(motif + '\t' + str(number) + '\t' + str(length) + '\t' + str(pre) + '\n')
