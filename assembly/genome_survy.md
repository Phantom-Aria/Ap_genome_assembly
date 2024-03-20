## Step1

**Generate quality inspection report for Illumina sequencing**

```
fastqc *.fq.gz -o ./
```



## Step2

**Filter Illumina sequencing data**

```
trim_galore -q 25 -phred33 -length 100 -stringency 1 -paired -o clean_data 1_raw_1.fq.gz 1_raw_2.fq.gz
```



## Step3

**run k-mer annalysis**

```
jellyfish count -m 17 -s 300M -t 50 -C -o 17-mer.jf ./1_raw_1_val_1.fq ./1_raw_2_val_2.fq
jellyfish histo -t 4 17-mer.jf > 17-mer.histo
jellyfish stats 17-mer.jf -o counts_stats.txt
```

