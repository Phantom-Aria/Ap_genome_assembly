## 01.Data_Pre-processing

### Step1.sh

```
#!/bin/bash
ref=$1

bwa-mem2 index $ref
samtools faidx $ref
referencename=`basename $ref | sed  "s/fasta/dict/" `		
gatk CreateSequenceDictionary -R $ref -O $referencename 
```

### Step2.sh

```
#!/bin/bash
sampleName=$1

gatk FastqToSam -F1 raw_fastq/${sampleName}_1.fq.gz -F2 raw_fastq/${sampleName}_2.fq.gz -RG $sampleName -SM $sampleName -O ubam/${sampleName}.bam

gatk MarkIlluminaAdapters -I ubam/${sampleName}.bam -O markadapeters/${sampleName}.markadapeters.bam -M markadapeters/${sampleName}.metrics.txt
```

### Step3.sh

```
#!/bin/bash
sampleName=$1
threads=50
ref=/public/home/wlxie/biosoft/GATK_file/gatk/ref/luobuma.fasta

gatk SamToFastq -I markadapeters/${sampleName}.markadapeters.bam -F  interleaved_fq/${sampleName}_1.interleaved.fq.gz -F2  interleaved_fq/${sampleName}_2.interleaved.fq.gz -CLIP_ATTR XT -CLIP_ACT 2

bwa-mem2 mem -M -t $threads $ref  interleaved_fq/${sampleName}_1.interleaved.fq.gz interleaved_fq/${sampleName}_2.interleaved.fq.gz | samtools view -Sb - > raw_bam/${sampleName}.bam

gatk MergeBamAlignment -R $ref -UNMAPPED  ubam/${sampleName}.bam -O align_bam/${sampleName}.bam -ALIGNED  raw_bam/${sampleName}.bam -MC true --CREATE_INDEX true

rm -rf markadapeters/${sampleName}.markadapeters.ba interleaved_fq/${sampleName}_1.interleaved.fq.gz  interleaved_fq/${sampleName}_2.interleaved.fq.gz raw_bam/${sampleName}.bam
```

### step4.sh

```
#!/bin/bash
sampleName=$1

gatk MarkDuplicates -I align_bam/${sampleName}.bam -O markdup/${sampleName}.markdup.bam -M markdup/${sampleName}.markdup_metrics.txt --CREATE_INDEX true

rm -rf  align_bam/${sampleName}.bam 
```



## 02.Variant_Discovery

### Step1.sh

```
#!/bin/bash
sampleName=$1
threads=50
ref=/public/home/wlxie/biosoft/GATK_file/gatk/ref/A.pictum.fasta

gatk HaplotypeCaller -R $ref --native-pair-hmm-threads ${threads} -I ../../pre_processing/markdup/${sampleName}.markdup.bam -O ${sampleName}.vcf.gz
```



## 03.Callset_Refinement

### Step1.sh

```
#!/bin/bash
sampleName=$1
threads=50
VARIANTS=/public/home/wlxie/biosoft/GATK_file/gatk/variants_discover/A.pictum/raw_variants.vcf.gz

# SNP
gatk SelectVariants -select-type SNP -V $VARIANTS --restrict-alleles-to BIALLELIC  -O ${sampleName}_SNP.vcf.gz
gatk VariantFiltration -V ${sampleName}_SNP.vcf.gz --filter-expression "QD < 2.0 || MQ < 40.0 || FS > 60.0 || SOR > 3.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0" --filter-name "Filter" -O ${sampleName}_SNP.filter.vcf.gz
gatk SelectVariants  -V ${sampleName}_SNP.filter.vcf.gz --exclude-filtered true -O final.${sampleName}_SNP.vcf.gz
rm -rf ${sampleName}_SNP.vcf.gz*
rm -rf ${sampleName}_SNP.filter.vcf.gz*

# INDEL
gatk SelectVariants -select-type INDEL -V $VARIANTS --restrict-alleles-to BIALLELIC  -O ${sampleName}_INDEL.vcf.gz
gatk VariantFiltration -V ${sampleName}_INDEL.vcf.gz --filter-expression "QD < 2.0 || FS > 200.0 || SOR > 10.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0" --filter-name "Filter" -O ${sampleName}_INDEL.filter.vcf.gz
gatk SelectVariants  -V ${sampleName}_INDEL.filter.vcf.gz --exclude-filtered true -O final.${sampleName}_INDEL.vcf.gz		
rm -rf ${sampleName}_INDEL.vcf.gz*
rm -rf ${sampleName}_INDEL.filter.vcf.gz*
```

