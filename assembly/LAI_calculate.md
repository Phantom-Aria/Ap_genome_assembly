**All the following scripts are executed in SLURM with the following parameters**

`#!/bin/bash`
`#SBATCH -n 120`



## Step1

```
ltr_finder -D 15000 -d 1000 -L 7000 -l 100 -p 20 -C -M 0.85 /public/home/wlxie/NextPolish/01_rundir/genome.nextpolish.fasta > baima_ltrfinder.scn
```



## Step2

```
gt suffixerator -db /public/home/wlxie/NextPolish/01_rundir/genome.nextpolish.fasta -indexname index/baima -tis -suf -lcp -des -ssp -sds -dna

gt ltrharvest -index index/baima -minlenltr 100 -maxlenltr 7000 -mintsd 4 -maxtsd 6 -motif TGCA -motifmis 1 -similar 85 -vic 10 -seed 20 -seqids yes > baima_ltrharvest.scn
```



## Step3

```
LTR_retriever -genome /public/home/wlxie/NextPolish/01_rundir/genome.nextpolish.fasta -inharvest baima_ltrharvest.scn -infinder baima_ltrfinder.scn -threads 20
```

