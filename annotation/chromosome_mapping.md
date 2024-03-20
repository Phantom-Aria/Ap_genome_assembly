## Step1

**Juicer configuration**

```
git clone https://ghproxy.com/https://github.com/aidenlab/juicer.git
cd juicer

ln -s CPU scripts

cd scripts/common
wget -c https://ghproxy.com/https://github.com/aidenlab/Juicebox/releases/download/v2.20.00/juicer_tools.2.20.00.jar

ln -s juicer_tools.2.20.00.jar juicer_tools.jar

mkdir reference && cd reference
cp /path/to/your/reference/genome.fa ./
bwa index genome.fa

mkdir restriction_sites && cd restriction_sites
python ~/biosoft/juicer/misc/generate_site_positions.py MboI genome ~/biosoft/juicer/reference/genome.fa

awk 'BEGIN{OFS="\t"}{print $1, $NF}' genome_MboI.txt > genome.chrom.sizes
```



## Step2

**Run juicer.slurm**

```
#!/bin/bash
#SBATCH -N 1
#SBATCH -n 30
#SBATCH -t 7200

/public/home/wlxie/biosoft/juicer/scripts/juicer.sh \
-z /public/home/wlxie/biosoft/juicer/reference/genome.fa \
-p /public/home/wlxie/biosoft/juicer/restriction_sites/genome.chrom.sizes \
-y /public/home/wlxie/biosoft/juicer/restriction_sites/genome_MboI.txt \
-s MboI \
-D /public/home/wlxie/biosoft/juicer \
-t 30 \
--assembly
```



## Step3

**3D-DNA configuration**

```
git clone https://ghproxy.com/https://github.com/aidenlab/3d-dna.git

chmod 755 run-asm-pipeline-post-review.sh
chmod 755 run-asm-pipeline.sh

conda install LastZ

wget http://ftp.gnu.org/gnu/parallel/parallel-latest.tar.bz2
tar -xvjf parallel-latest.tar.bz2
cd parallel-20230622
./configure --prefix=$HOME && make && make install
```



## Step4

**Run 3d-dna.slurm**

```
#!/bin/bash
#SBATCH -n 30
#SBATCH -N 1
#SBATCH -t 7200

/public/home/wlxie/biosoft/3d-dna/run-asm-pipeline.sh \
		/public/home/wlxie/biosoft/juicer/reference/genome.fa \
		-r 0 \
		/public/home/wlxie/biosoft/juicer/aligned/merged_nodups.txt

```



## Step5

**Run run-asm-pipeline-post-review.sh (after JBAT)**

```
#!/bin/bash
#SBATCH -n 30
#SBATCH -N 1
#SBATCH -t 7200

/public/home/wlxie/biosoft/3d-dna/run-asm-pipeline-post-review.sh \
         -r /public/home/wlxie/biosoft/3d-dna/baima_diploid/genome_rawchrom.review.assembly \
         /public/home/wlxie/biosoft/juicer/reference/genome.fa \
         /public/home/wlxie/biosoft/juicer/aligned/merged_nodups.txt

```



## Step6

**Statistics of genome assembly information (use custom python script)**

```python
fasta_file = 'genome.FINAL.fasta'	

def fasta_length(file_path):
    sequences = {}
    with open(file_path, 'r') as file:
        content = file.read() 

    blocks = content.split('>')  

    for block in blocks[1:]:   
        index = block.find('\n')   
        newline_number = block.count('\n')   
        header = block[:index] 
        sequence_length = len(block) - index - newline_number   
        sequences[header] = sequence_length
    return sequences

sequence_lengths = fasta_length(fasta_file)

for header, length in sequence_lengths.items():
    print(f'{header}:{length}')
```



## Step7

**Make Hi-C heatmap**

```
#!/bin/bash
#SBATCH -n 8
#SBATCH -t 7200

assembly=/public/home/wlxie/biosoft/3d-dna/baima_diploid/genome_rawchrom.review.assembly
merged_nodups=/public/home/wlxie/biosoft/juicer/aligned/merged_nodups.txt

./juicerbox2matrix -a ${assembly} -c 11 -i ${merged_nodups} -o run

plotHicGenome juicer ${merged_nodups} ${assembly} -H run/Hicmatrix.txt -W whole -n 11 -s False -l t -F 4 -r 500000 -X 2 -w 0.5 -d 3 -S 'dashed' -i 300 -z 6,6 -C 'black' -L 0.8 -A 0.8 -B '1%' -D 0.2 -o Juicerbox.pdf -R ./run

```

