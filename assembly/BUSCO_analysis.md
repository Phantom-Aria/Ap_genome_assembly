## Step1

**download eudicots database**

```
nohup wget https://busco-data.ezlab.org/v5/data/lineages/eudicots_odb10.2020-09-10.tar.gz &
tar -zxvf eudicots_odb10.2020-09-10.tar.gz
```



## Step2

**assembly result run BUSCO**

```
busco -i /public/home/wlxie/NextPolish/01_rundir/genome.nextpolish.fasta -l /public/home/wlxie/busco_soft/busco/test_data/eukaryota/busco_downloads/lineages/eudicots_odb10 -o baima -m genome --cpu 8 --offline
```



## Step3 (after genome annotation)

**annotation result run BUSCO **

```
database_path=/public/home/wlxie/biosoft/busco_soft/busco/test_data/eukaryota/busco_downloads/lineages/eudicots_odb10
sequence_path=/public/home/wlxie/biosoft/braker3/Ap_mydb/Ap_rmTE.aa

busco -i ${sequence_path} -l ${database_path} -o Ap -m proteins --cpu 8 --offline
```

