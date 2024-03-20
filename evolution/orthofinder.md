## Step1

**Run orthofinder**

```
#!/bin/bash
#SBATCH -n 5
#SBATCH -t 7200

python ./orthofinder.py -M msa -f mydata/ -t 5
```



## Step2

**Convert multiple sequence alignment file to PHYLIP format**

```python
# custom python script
def protein_sequence(file_path):
    sequences = {}
    with open(file_path, 'r') as file:
        content = file.read()
    blocks = content.split('>')     
    for block in blocks[1:]:
        index = block.find('\n')
        header = block[:index]
        sequence = block[index + 1: -1].replace('\n', '')
        sequences[header] = sequence
    return sequences

sequences = protein_sequence('./mcmctree/SpeciesTreeAlignment.fa')

species_number = len(sequences)
sequence_length = len(sequences[next(iter(sequences))])  


with open('mcmctree.phylip', 'w') as f:
    f.write(f'{species_number} {sequence_length}\n')
    for key, value in sequences.items():
        f.write(f'{key}  {value}\n')
```



## step3

**MCMCtree  configuration**

```
          seed = -1
       seqfile = mcmctree.phylip
      treefile = mcmctree.tree
       outfile = mcmc.out

         ndata = 1
       seqtype = 2  * 0: nucleotides; 1:codons; 2:AAs
       usedata = 3    * 0: no data; 1:seq like; 2:use in.BV; 3: out.BV
         clock = 3    * 1: global clock; 2: independent rates; 3: correlated rates
       RootAge = <2.0  * safe constraint on root age, used if no fossil for root.

         model = 2    * 0:JC69, 1:K80, 2:F81, 3:F84, 4:HKY85
         alpha = 0    * alpha for gamma rates at sites
         ncatG = 5    * No. categories in discrete gamma
    aaRatefile = wag.dat

     cleandata = 0    * remove sites with ambiguity data (1:yes, 0:no)?

       BDparas = 1 1 0    * birth, death, sampling
   kappa_gamma = 6 2      * gamma prior for kappa
   alpha_gamma = 1 1      * gamma prior for alpha

   rgene_gamma = 2 2   * gamma prior for overall rates for genes
  sigma2_gamma = 1 10    * gamma prior for sigma^2     (for clock=2 or 3)

      finetune = 1: 0.1  0.1  0.1  0.01 .5  * auto (0 or 1) : times, musigma2, rates, mixing, paras, FossilErr

         print = 1
        burnin = 8000
      sampfreq = 2
       nsample = 200000

*** Note: Make your window wider (100 columns) before running the program.
```



## Step4

**Run MCMCtree twice**

```
mv out.BV in.BV

# step3
usedata = 2
```



## step5

**CAFE**

```
awk 'OFS="\t" {$NF=""; print}' Orthogroups.GeneCount.tsv > tmp && awk '{print "(null)""\t"$0}' tmp > cafe.input.tsv && sed -i '1s/(null)/Desc/g' cafe.input.tsv && rm tmp

python cafetutorial_clade_and_size_filter.py -i cafe.input.tsv -o gene.families.filtered.tsv -s 2> filtered.log

cafe5 -i gene.families.filtered.tsv -t tree.txt -c 10 -p -k 5 -o k5p
```

