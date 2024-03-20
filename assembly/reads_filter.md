## Step1

**Generate quality inspection report**

```
NanoPlot --summary summary.txt --loglength -o summary-plots-log-transformed
NanoPlot -t 4 --fastq pass.fq.gz --plots hex dot -o nanoplot_out
```



## Step2

**Filter sequencing data**

```
filtlong --min_length 1000 pass.fq.gz | gzip > clean_filter.fq.gz
```



## Step3

**Generate quality inspection report again**

```
NanoPlot -t 4 --fastq clean_filter.fq.gz --plots hex dot -o filt_nanoplot_out
```