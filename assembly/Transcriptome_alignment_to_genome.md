## Step1

**Transcriptome alignment to genome**

```
#!/bin/bash
#SBATCH -n 20

genome_path=/public/home/wlxie/Genome/Ap.fasta
gff3_path=/public/home/wlxie/biosoft/braker3/Ap_rmTE.gff3
fq_path=/public/home/wlxie/Sequencing_data/BYT2022020901/Apocynum_pictum/

# hisat2 
hisat2-build ${genome_path} genome
hisat2 -p 20 -x genome -S out.sam  -1 ${fq_path}1.fq -2 ${fq_path}2.fq

# samtools transfer sam to bam and sort
samtools sort -@ 20 -o out.bam out.sam

# Quantitative analysis
stringtie -p 20 -e -G ${gff3_path} -o result.gtf out.bam

# Delete temporary files
rm -rf genome.*
rm -rf out.*
```



## Step2

**Statistical results with custom python script**

```python
# calculate.py
## Calculate the number of genes with TPM values greater than 0.001.

count = 0
gen_count = 0
with open('result.gtf', 'r') as gtf:
    lines = gtf.readlines()
    for line in lines:
        if "TPM" in line:
            gen_count += 1
            TPM = line.split('\t')[8].split(';')[4].split(' ')[2]
            TPM = float(TPM.strip('"'))
            if TPM > 0.001:
                count += 1
print(f'Total gene number：{gen_count} \nNumber of genes with expression greater than 0.001：{count}')
print(f'占比：{count/gen_count*100:.2f} %')
```

