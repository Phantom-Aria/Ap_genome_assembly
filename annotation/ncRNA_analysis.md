## Step1

**Download Rfam database** 

```
wget ftp://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT/Rfam.cm.gz
wget ftp://ftp.ebi.ac.uk/pub/databases/Rfam/CURRENT/Rfam.clanin

gunzip Rfam.cm.gz
cmpress Rfam.cm
```



## Step2

**Run Infernal**

```
#!/bin/bash
#SBATCH -n 50
#SBATCH -t 7200

cmscan --cut_ga --rfam --nohmmonly --tblout luobuma.tblout --fmt 2 -o luobuma.out --clanin Rfam.clanin Rfam.cm /public/home/wlxie/NextPolish/rundir/A.pictum.nextpolish.fasta
```



## Step3

**Statistics of predicted ncRNA results (based on Rfam website)**

```python
'''
Statistics.py
Statistics of predicted ncRNA results
accession.txt from Rfam website
2023.3.22
'''

loci_length = []
accession = []
with open('./luobuma.tblout', 'r') as input:
    for i in input.readlines():
        if i.find('#') != -1 or i.find('=') != -1 or i.find('$') != -1:
            continue
        else:
            lst = i.strip().split()
            if len(lst) < 1:
                continue
            length = abs(int(lst[10]) - int(lst[9]))
            loci_length.append(length)
            accession.append(lst[2])
len_sum = 0
for i in loci_length:
    len_sum += i

accession_num = []
dicts = {}
with open('./accession.txt', 'r') as ac:
    for i in ac.readlines():
        m = i.strip().split('\t')		
        accession_num.append(m[0])
        nc_type = m[2].split(';')[1].strip()	
        if m[0] not in dicts:
            dicts[m[0]] = nc_type

mi = s = sn = lnc = t = r = other = 0
mi_len = s_len = sn_len = lnc_len = t_len= r_len = other_len =0
for i in range(len(accession)):
    item = accession[i]
    if item in dicts:
        if dicts[item] == 'miRNA':
            mi += 1
            mi_len += int(loci_length[i])
        elif dicts[item] == 'sRNA':
            s += 1
            s_len += int(loci_length[i])
        elif dicts[item] == 'snRNA':
            sn += 1
            sn_len += int(loci_length[i])
        elif dicts[item] == 'lncRNA':
            lnc += 1
            lnc_len += int(loci_length[i])
        elif dicts[item] == 'tRNA':
            t += 1
            t_len += int(loci_length[i])
        else:
            r += 1
            r_len += int(loci_length[i])
    else:
        other += 1
        other_len += int(loci_length[i])

outputlst = [('miRNA', mi, mi_len), ('sRNA', s, s_len), ('snRNA', sn, sn_len), ('lncRNA', lnc, lnc_len), ('tRNA', t, t_len), ('rRNA', r, r_len), ('others', other, other_len), ('total', len(accession), len_sum)]

with open('./res.xls', 'w') as output:
    output.write('Type\tCopy Number\tTotal length(bp)\n')
    for i in outputlst:
        type = str(i[0])
        number = str(i[1])
        length = str(i[2])
        output.write(type + '\t' + number + '\t' + length + '\n')
```

