## Step1

**Download database**

```
nohup wget https://v100.orthodb.org/download/odb10_plants_fasta.tar.gz &
tar zxvf odb10_plants_fasta.tar.gz
cat plants/Rawdata/* > plant_proteins.faa

# TAIR10.1
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_protein.faa.gz
# Ntab-TN90
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/715/135/GCF_000715135.1_Ntab-TN90/GCF_000715135.1_Ntab-TN90_protein.faa.gz
# IRGSP-1.0
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/001/433/935/GCF_001433935.1_IRGSP-1.0/GCF_001433935.1_IRGSP-1.0_protein.faa.gz
# coffea arabica
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/003/713/225/GCF_003713225.1_Cara_1.0/GCF_003713225.1_Cara_1.0_protein.faa.gz
# coffea canephora
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/900/059/795/GCA_900059795.1_AUK_PRJEB4211_v1/GCA_900059795.1_AUK_PRJEB4211_v1_protein.faa.gz

gunzip *.gz
cat *.faa > mydb_proteins.fasta
```



## Step2

**Run Braker singularity**

```
#!/bin/bash
#SBATCH -n 48
#SBATCH -t 7200

wd=baima_pre

if [ -d $wd ]; then
    rm -r $wd
fi

singularity exec -B ${PWD}:${PWD} ${BRAKER_SIF} braker.pl --genome=/public/home/wlxie/biosoft/db_data/baima/RepeatMasker_soft/genome.nextpolish.fasta.masked --prot_seq=mydb_proteins.fasta --softmasking --threads 48 --workingdir=${wd} --rnaseq_sets_dirs=/public/home/wlxie/RNAseq/BYT2022020901/rnaseq/baima --rnaseq_sets_ids=4-216031965_raw

```



## Step3

**Remove DNA inserted by TE**

```
#!/bin/bash
#SBATCH -n 8
#SBATCH -t 7200

TEsorter /public/home/wlxie/baima_pre_mydb/braker.codingseq -eval 1e-6 -p 8

grep -v "^#" braker.codingseq.rexdb.cls.tsv | cut -f1 | sort | uniq | cut -f1 -d "_" | sort | uniq > TE-genes.txt

grep -Fvf /public/home/wlxie/biosoft/TEsorter/Ap_mydb/TE-genes.txt final.gff3 > Ap_rmTE.gff3

gffread Ap_rmTE.gff3 -g ~/Genome/Ap.fasta -x Ap_rmTE.codingseq
gffread Ap_rmTE.gff3 -g ~/Genome/Ap.fasta -y Ap_rmTE.aa

cat Ap_rmTE.gff3 | awk '{if ($3=="gene") print $0}' | awk '{sum+=($5 -$4)} END {print sum, NR, sum/NR}'
```

