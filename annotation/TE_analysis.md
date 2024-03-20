## Step1

**Export library of repetitive sequences from homologous species**

```
python famdb.py -i Libraries/RepeatMaskerLib.h5 lineage -ad lamiids	

python famdb.py -i Libraries/RepeatMaskerLib.h5 families -f embl -a -d lamiids > lamiids.embl	

buildRMLibFromEMBL.pl lamiids.embl > lamiids.fasta	
```



## Step2

**RepeatModeler de novo predition**

```
#!/bin/bash
#SBATCH -n 100
#SBATCH -t 7200

BuildDatabase -name luobuma -engine ncbi /public/home/wlxie/NextPolish/luobuma_rundir/genome.nextpolish.fasta

RepeatModeler -pa 25 -database luobuma -engine ncbi

cat lamiids.fasta luobuma-families.fa luobuma.fasta.mod.LTRlib.fa > final_luobuma_repeat.fasta
```



## Step3

**RepeatMasker search for repetitive sequences**

```
#!/bin/bash
#SBATCH -n 100
#SBATCH -t 7200

RepeatMasker -nolow -no_is -pa 25 -lib final_luobuma_repeat.fasta -engine ncbi -gff -norna -dir luobuma /public/home/wlxie/NextPolish/rundir/A.pictum.fasta 
```

